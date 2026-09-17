# core — retro-ADRs (NetBox @ ea4c205)

## ADR-1: Change logging is a global signal receiver, gated by a request context variable

**Context.** Every NetBox model that supports change logging needs an `ObjectChange` written on create, update, M2M change and delete, without each app wiring its own hooks [code:netbox/core/signals.py:41-46].

**Decision.** `core.signals` registers `handle_changed_object` on `post_save` and `m2m_changed` and `handle_deleted_object` on `pre_delete` with no `sender` filter; the receivers opt in by duck-typing (`hasattr(instance, 'to_objectchange')`) and bail out when `current_request.get()` is `None` [code:netbox/core/signals.py:45-58] [code:netbox/core/signals.py:111-131]. Deletion also runs configured `PROTECTION_RULES` before anything is queued, and manually emulates reverse-M2M and nullable-FK changes on related change-logged objects because Django does not signal them [code:netbox/core/signals.py:116-126] [code:netbox/core/signals.py:142-171].

**Consequences.** Anything saved outside a request context (shell, jobs, migrations) produces no change record and no event; code paths that want silence exploit exactly this by using `QuerySet.update()` (see ADR-5) [code:netbox/core/signals.py:55-58] [code:netbox/core/models/data.py:172-173]. M2M edits within one request are folded into the earlier `ObjectChange` for the same object and `request_id` rather than creating a second row [code:netbox/core/signals.py:79-89]. Event enqueueing for `extras` is coupled into these receivers, so `core` imports `extras.events` and `extras.utils`, an upward dependency [fg:imports:core.signals->extras.events] [fg:imports:core.signals->extras.utils]. The behaviour is tested against `dcim` models, not core's, which is what a global receiver implies [fg:imports:core.tests.test_changelog->dcim.models].

## ADR-2: `ObjectType` is a proxy of `ContentType` whose manager consults the registry

**Context.** Many features need "the content types that support X" (jobs, change logging, custom fields, permissions) and "the public models" [code:netbox/core/models/contenttypes.py:14-31].

**Decision.** Migration `0008` creates `ObjectType` as a `proxy = True` subclass of `contenttypes.ContentType` with `ObjectTypeManager`, whose `public()` and `with_feature()` build `Q` objects from `registry['models']` and `registry['model_features']` [code:netbox/core/migrations/0008_contenttype_proxy.py:11-24] [code:netbox/core/models/contenttypes.py:12-50]. `CoreConfig.ready()` registers core's models into that registry via `register_models` [code:netbox/core/apps.py:26-31].

**Consequences.** Foreign keys to the proxy appear across `extras` and `users` (`CustomField.object_types`, `EventRule.object_types`, `ObjectPermission.object_types`), so the proxy is a schema dependency and its `app_label`/table stay `contenttypes` [fg:model_refs:extras.models.customfields:74] [fg:model_refs:extras.models.models:51] [fg:model_refs:users.models.permissions:31]. Core's own models still declare their FKs to `contenttypes.ContentType`, not to the proxy, and validate at `clean()` time with `with_feature()` [fg:model_refs:core.models.jobs:31] [code:netbox/core/models/jobs.py:133-140] [code:netbox/core/models/change_logging.py:117-126]. `with_feature()` raises `KeyError` for an unregistered feature name, so feature names are effectively an API [code:netbox/core/models/contenttypes.py:31-34].

## ADR-3: `ObjectChange` and `ConfigRevision` were moved from `extras` to `core` with state-only migrations

**Context.** Both models predate `core` and lived in `extras` [code:netbox/core/migrations/0011_move_objectchange.py:75-76] [code:netbox/core/migrations/0009_configrevision.py:27-28].

**Decision.** Migrations `0009` and `0011` wrap `CreateModel` in `SeparateDatabaseAndState` with empty `database_operations`; the physical table rename is done in `extras` migrations, which the comments name [code:netbox/core/migrations/0009_configrevision.py:10-29] [code:netbox/core/migrations/0011_move_objectchange.py:14-17]. The initial squashed migration already depends on `extras.0002_squashed_0059`, so the two apps' histories are interleaved [code:netbox/core/migrations/0001_squashed_0005.py:19-23].

**Consequences.** Migration ordering between `core` and `extras` is load-bearing in both directions, and any further model move must follow the same two-sided pattern. Old `extras` migrations still resolve core models by name (`get_model('core', 'Job')`) [fg:model_refs:extras.migrations.0108_convert_reports_to_scripts:6] [fg:model_refs:extras.migrations.0109_script_model:90].

## ADR-4: `Job` is a database mirror of an RQ job, keyed by a shared UUID, enqueued on commit

**Context.** Background work needs a durable, queryable record with a user, status and result while RQ owns execution [code:netbox/core/models/jobs.py:27-30].

**Decision.** `Job.enqueue()` creates and `full_clean()`s a row with `job_id=uuid4()`, then hands `func` to RQ with the same `job_id` inside `transaction.on_commit`, either `enqueue` or `enqueue_at`; `immediate=True` runs synchronously instead [code:netbox/core/models/jobs.py:245-273]. Queue selection comes from `get_queue_for_model(object_type.model)` unless overridden [code:netbox/core/models/jobs.py:242-243]. `Job.delete()` cancels the RQ job after the row is gone, tolerating `InvalidJobOperation` [code:netbox/core/models/jobs.py:157-169]. `start()`/`terminate()` update status and emit `job_start`/`job_end`, which `extras` consumes for event rules [code:netbox/core/models/jobs.py:171-206] [code:netbox/extras/signals.py:96-97] [fg:imports:extras.signals->core.signals].

**Consequences.** If the surrounding transaction rolls back, no RQ job is ever enqueued and the `Job` row disappears with it. `object_type` was later made nullable (`0012`) so jobs need not be bound to an object, enabling `@system_job` classes that `rqworker` schedules at startup via `enqueue_once` [code:netbox/core/migrations/0012_job_object_type_optional.py:12-22] [code:netbox/core/management/commands/rqworker.py:19-26] [code:netbox/core/jobs.py:40-46]. `Job.get_absolute_url` still hard-codes routes for `reportmodule` and `scriptmodule`, flagged with a TODO [code:netbox/core/models/jobs.py:121-128]. The raw-RQ admin screens (`BaseRQView`, `BaseRQViewSet`) operate on RQ objects directly and are staff/admin-only, a separate surface from the `Job` model [code:netbox/core/views.py:343-346] [code:netbox/core/api/views.py:88-92].

## ADR-5: DataSource status changes bypass `save()` and signals

**Context.** Syncing flips `status` several times (`QUEUED`, `SYNCING`, `COMPLETED`/`FAILED`) and these transitions should not produce change-log entries, events or trigger `enqueue_sync_job` [code:netbox/core/signals.py:196-204].

**Decision.** All status writes use `DataSource.objects.filter(pk=...).update(...)`: in `sync()`, `DataSourceSyncView.post`, the API `sync` action, `SyncDataSourceJob.run` and `syncdatasource` [code:netbox/core/models/data.py:172-173] [code:netbox/core/models/data.py:224-226] [code:netbox/core/views.py:84-85] [code:netbox/core/api/views.py:55-56] [code:netbox/core/jobs.py:34] [code:netbox/core/management/commands/syncdatasource.py:42].

**Consequences.** `status` and `last_synced` never appear in the changelog, and the in-memory instance is updated by hand alongside the query. `pre_sync`/`post_sync` are the only hooks around a sync; `auto_sync` uses `post_sync` to push file content into every `AutoSyncRecord`-mapped object [code:netbox/core/models/data.py:169-170] [code:netbox/core/models/data.py:228-229] [code:netbox/core/signals.py:215-223].

## ADR-6: Data backends are registry plugins; `DataSource.type` is a free string with JSON parameters

**Context.** Backends (local, git, S3, plugin-provided) need their own credentials and optional dependencies [code:netbox/core/data_backends.py:43-66] [code:netbox/core/data_backends.py:127-141].

**Decision.** Migration `0006` removed DB-level choices from `type`; validity is checked in `clean()` against `registry['data_backends']`, and each backend declares `parameters` as Django form fields and `sensitive_parameters` [code:netbox/core/migrations/0006_datasource_type_remove_choices.py:11-17] [code:netbox/core/models/data.py:122-126] [code:netbox/core/data_backends.py:47-66]. `DataSourceForm` injects `backend_<name>` fields at runtime and packs them back into `parameters` on save [code:netbox/core/forms/model_forms.py:66-90]. `to_objectchange` censors sensitive parameters with `CENSOR_TOKEN`/`CENSOR_TOKEN_CHANGED` [code:netbox/core/models/data.py:134-154].

**Consequences.** Credentials live in a JSON column in plaintext; only the changelog copy is censored, and the bulk-edit form exposes `parameters` as raw JSON [code:netbox/core/forms/bulk_edit.py:39-42]. Missing optional libraries surface at sync time as `SyncError`, not at configuration time [code:netbox/core/models/data.py:176-181]. `DataFile` rows are owned exclusively by `sync()` (bulk create/update/delete) and are read-only everywhere else [code:netbox/core/models/data.py:263-267] [code:netbox/core/models/data.py:202-221] [fg:symbols:core.api.views:DataFileViewSet].

## ADR-7: Dynamic configuration is a JSON revision activated into the cache by a signal

**Context.** Some settings must be editable at runtime without touching `configuration.py` [code:netbox/core/models/config.py:13-16].

**Decision.** `ConfigRevision.data` holds a dict of parameter values; `activate()` writes it and the pk into the cache keys `config`/`config_version`, and a `post_save` receiver activates every newly saved revision [code:netbox/core/models/config.py:56-66] [code:netbox/core/signals.py:226-231]. `netbox.config` reads the cache and falls back to the latest row [code:netbox/netbox/config/__init__.py:70-80]. `ConfigRevisionForm` is generated by a metaclass from `PARAMS`, and any parameter also set statically in `settings` is rendered disabled [code:netbox/core/forms/model_forms.py:127-146] [code:netbox/core/forms/model_forms.py:207-213].

**Consequences.** "Restore" is simply `activate()` on an older row; `is_active` is a cache comparison, so a cache flush makes no revision active until the next load [code:netbox/core/views.py:328-336] [code:netbox/core/models/config.py:64-66]. `ConfigRevision.__getattr__` resolves attribute access from `data`, so revisions behave like settings objects in templates [code:netbox/core/models/config.py:46-49].

## ADR-8: Core patches Django's migration machinery and gates `makemigrations`

**Context.** Cosmetic `verbose_name` edits and NetBox-specific field attributes were generating noise migrations [code:netbox/core/apps.py:12-16].

**Decision.** At import, `apps.py` removes `verbose_name`/`verbose_name_plural` from `AlterModelOptions.ALTER_OPTION_KEYS` and replaces `models.Field.deconstruct` with `utilities.migration.custom_deconstruct`; the overridden `makemigrations` refuses to run unless `settings.DEVELOPER` or `--check` [code:netbox/core/apps.py:13-17] [code:netbox/core/management/commands/makemigrations.py:8-22]. A system check flags an index duplicating a unique constraint, and `0015` removed three such indexes [code:netbox/core/checks.py:10-41] [code:netbox/core/migrations/0015_remove_redundant_indexes.py:10-22].

**Consequences.** Migration autodetection in NetBox differs from stock Django for every app, including plugins, and depends on `core` being loaded first [fg:imports:core.apps->utilities.migration].
