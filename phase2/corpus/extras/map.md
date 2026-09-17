# extras — map (NetBox ea4c205, 2 July 2025)

## What it is

`extras` is the Django app that holds NetBox's cross-cutting "feature" machinery rather than a domain of its own: custom fields, tags, custom links, export/config templates, config contexts, saved filters, table configs, bookmarks, journaling, image attachments, event rules with webhook/script/notification actions, notifications and subscriptions, user dashboards, the custom-script framework, the search cache, and five management commands. It is 106 modules, 22,120 lines of code plus 121,327 lines of data tables, with 15 test modules. [fg:subsystems:extras]

The data lines are three static choice lists (IATA, ISO 3166, UN/LOCODE) that back the "base choices" of `CustomFieldChoiceSet`; `un_locode.py` alone is 111,558 lines. [fg:modules:extras.data.un_locode] [code:netbox/extras/data/__init__.py:1-9] [code:netbox/extras/models/customfields.py:815-828]

## Modules by role

**Models** (`extras/models/`, re-exported through `models/__init__.py` star-imports). `models.py` holds EventRule, Webhook, CustomLink, ExportTemplate, SavedFilter, TableConfig, ImageAttachment, JournalEntry, Bookmark; `customfields.py` holds CustomField, CustomFieldChoiceSet and CustomFieldManager; `configs.py` holds ConfigContext, the abstract ConfigContextModel, and ConfigTemplate; `notifications.py` holds Notification, NotificationGroup, Subscription; `scripts.py` holds Script and the ScriptModule proxy; `tags.py` holds Tag/TaggedItem; `search.py` holds CachedValue; `dashboard.py` holds Dashboard; `mixins.py` holds PythonModuleMixin and RenderTemplateMixin. [code:netbox/extras/models/__init__.py:1-8] [fg:modules:extras.models.models] [fg:modules:extras.models.customfields] [fg:modules:extras.models.configs] [fg:modules:extras.models.mixins]

**Views**: `views.py` (1,539 lines, 121 classes) is one flat file of per-model CRUD view families registered with `@register_model_view`, plus non-generic views for notifications, dashboard widgets, scripts and Markdown preview. [fg:modules:extras.views] [code:netbox/extras/views.py:45-100] [code:netbox/extras/views.py:1108-1133]

**Forms**: split by purpose into `model_forms.py`, `bulk_edit.py`, `bulk_import.py`, `filtersets.py`, `scripts.py`, `reports.py`, `misc.py`, all star-re-exported by the package `__init__`. [fg:modules:extras.forms.model_forms] [fg:modules:extras.forms.bulk_edit] [fg:modules:extras.forms.bulk_import] [fg:modules:extras.forms.filtersets]

**Tables**: `tables/tables.py` (21 classes; 18 `NetBoxTable` subclasses plus `ScriptResultsTable`, `ReportResultsTable` on `BaseTable` and `ScriptJobTable` on core's `JobTable`) and a single custom column in `tables/columns.py`. [fg:symbols:extras.tables.tables:ScriptJobTable] [fg:symbols:extras.tables.tables:ReportResultsTable] [fg:symbols:extras.tables.columns:NotificationActionsColumn]

**Filtersets**: `filtersets.py` (19 classes) plus `filters.py`, which defines the `TagFilter`/`TagIDFilter` conjoined filters that `netbox.filtersets` mixes into every model filterset. [fg:modules:extras.filtersets] [code:netbox/extras/filters.py:11-38] [fg:imports:netbox.filtersets->extras.filters]

**REST API**: `api/views.py` (22 viewsets), `api/urls.py` (NetBoxRouter with 20 registrations plus a `dashboard/` path), one serializer module per model under `api/serializers_/` re-exported by `api/serializers.py`, `api/customfields.py` (the `custom_fields` serializer field used by every model serializer), and `api/mixins.py` (config-context/template rendering mixins used by dcim and virtualization viewsets). [code:netbox/extras/api/urls.py:7-35] [code:netbox/extras/api/serializers.py:1-16] [fg:imports:netbox.api.serializers.features->extras.api.customfields] [fg:imports:dcim.api.views->extras.api.mixins]

**GraphQL**: `graphql/types.py` (16 strawberry types), `graphql/filters.py` (14), `graphql/filter_mixins.py` and `graphql/mixins.py` (feature mixins consumed by every other app's types), `graphql/schema.py` (`ExtrasQuery`), `graphql/enums.py`. [fg:modules:extras.graphql.types] [code:netbox/extras/graphql/schema.py:9-57] [fg:imports:dcim.graphql.types->extras.graphql.mixins]

**Event pipeline**: `events.py` (queue, rule evaluation, dispatch), `webhooks.py` (RQ job that sends HTTP), `conditions.py` (JSON rule evaluator), `jobs.py` (`ScriptJob` runner), `signals.py` (custom-field data maintenance, custom validators, tag restriction, job event rules, notifications). [code:netbox/extras/events.py:97-153] [code:netbox/extras/webhooks.py:27-46] [code:netbox/extras/signals.py:140-174]

**Script framework**: `scripts.py` (ScriptVariable family, BaseScript, Script), `reports.py` (legacy Report shim), `storage.py` (script storage rooted at `SCRIPTS_ROOT`), `models/mixins.py` (`CustomStoragesLoader` executes module source via django-storages). [code:netbox/extras/scripts.py:286-296] [code:netbox/extras/reports.py:9-34] [code:netbox/extras/storage.py:6-14] [code:netbox/extras/models/mixins.py:21-35]

**Dashboard**: `dashboard/widgets.py` (base class + five registered widgets), `dashboard/utils.py` (registry, default dashboard), `dashboard/forms.py`, `constants.DEFAULT_DASHBOARD`. [code:netbox/extras/dashboard/widgets.py:98-154] [code:netbox/extras/dashboard/utils.py:18-36] [code:netbox/extras/constants.py:25-32]

**Search**: `search.py` registers indexes for CustomField, JournalEntry, Tag, Webhook; `models/search.py` is the `CachedValue` table that `netbox.search.backends` reads and writes; `fields.py`/`lookups.py` add the `empty` and `net_contains_or_equals` lookups. [code:netbox/extras/search.py:5-15] [fg:imports:netbox.search.backends->extras.models] [code:netbox/extras/lookups.py:33-34]

**Management commands**: `housekeeping`, `reindex`, `renaturalize`, `runscript`, `webhook_receiver`. [fg:entrypoints:extras.management.commands.housekeeping] [fg:entrypoints:extras.management.commands.reindex] [fg:entrypoints:extras.management.commands.renaturalize] [fg:entrypoints:extras.management.commands.runscript] [fg:entrypoints:extras.management.commands.webhook_receiver]

**Migrations**: 35 files; four squashed bundles cover 0001–0098, then 0099–0129 are live. [fg:modules:extras.migrations.0001_squashed] [fg:modules:extras.migrations.0087_squashed_0098] [fg:modules:extras.migrations.0129_fix_script_paths]

**Tests**: 15 modules; `test_customfields` (1,706 lines), `test_filtersets` (1,547), `test_api` (1,138) and `test_views` (810) dominate. [fg:modules:extras.tests.test_customfields] [fg:modules:extras.tests.test_filtersets] [fg:modules:extras.tests.test_api] [fg:modules:extras.tests.test_views]

## Entry points

Two URL modules (`extras.urls`, `extras.api.urls`), the API viewsets, the signals module, and the five commands. [fg:entrypoints:extras.urls] [fg:entrypoints:extras.api.urls] [fg:entrypoints:extras.api.views] [fg:entrypoints:extras.signals]

`ExtrasConfig.ready()` imports `dashboard`, `lookups`, `search`, `signals` for their side effects and calls `register_models()` on every model in the app. [code:netbox/extras/apps.py:7-12]

UI URLs are built almost entirely by `get_model_urls()`; the hand-written exceptions are the notifications HTMX list, dashboard widget views, script views (which accept either `<int:pk>` or `<module>.<name>`), and `render/markdown/`. [code:netbox/extras/urls.py:10-11] [code:netbox/extras/urls.py:62-89]

## What it depends on

Outbound imports by target: extras 186, utilities 98, netbox 96, core 63, dcim 30, users 17, tenancy 11, virtualization 11, ipam 5, circuits 4, wireless 1. [fg:subsystems:extras]

The dcim/virtualization/tenancy dependency is concentrated in config contexts: `ConfigContext` has twelve M2M fields to Region, SiteGroup, Site, Location, DeviceType, DeviceRole, Platform, ClusterType, ClusterGroup, Cluster, TenantGroup, Tenant, mirrored in its filterset, form, serializer and GraphQL type. [fg:model_refs:extras.models.configs:50] [fg:model_refs:extras.models.configs:105] [fg:imports:extras.filtersets->dcim.models] [fg:imports:extras.api.serializers_.configcontexts->dcim.api.serializers_.sites] [fg:imports:extras.graphql.types->dcim.graphql.types]

`ConfigTemplateListView` also counts Device, VirtualMachine, DeviceRole and Platform relations, and `scripts.py` reaches into `ipam.formfields`/`ipam.validators` for the IP variable types. [code:netbox/extras/views.py:869-884] [fg:imports:extras.scripts->ipam.formfields]

Almost every model targets `core.ObjectType` (`object_types` M2M on CustomField, CustomLink, ExportTemplate, SavedFilter, EventRule, Tag; FK on TableConfig and CustomField.related_object_type), while generic-FK models point at `contenttypes.ContentType`. [fg:model_refs:extras.models.customfields:74] [fg:model_refs:extras.models.models:292] [fg:model_refs:extras.models.models:533] [fg:model_refs:extras.models.models:648] [fg:model_refs:extras.models.notifications:52]

## What depends on it

Inbound imports by source: netbox 36, dcim 23, virtualization 17, utilities 12, core 5, plus account, circuits, tenancy, vpn, ipam, users. [fg:subsystems:extras]

The `netbox` package is the heaviest client: `netbox.models.features` imports `extras.choices`, `extras.constants`, `extras.utils` at module level and `extras.models.CustomField` lazily inside four methods; `netbox.filtersets` builds a filter per CustomField at runtime; `netbox.search.backends` reads `CachedValue`; `netbox.views.misc` renders the dashboard; `netbox.context_managers` flushes events. [fg:imports:netbox.models.features->extras.choices] [fg:imports:netbox.models.features->extras.models] [code:netbox/netbox/filtersets.py:294-307] [fg:imports:netbox.search.backends->extras.models] [fg:imports:netbox.views.misc->extras.dashboard.utils] [fg:imports:netbox.context_managers->extras.events]

`core.signals` imports `enqueue_event` and `run_validators`, so the change-logging signal handlers in core call into extras on every save. [fg:imports:core.signals->extras.events] [fg:imports:core.signals->extras.utils] [code:netbox/core/signals.py:13-14]

dcim and virtualization inherit `ConfigContextModel`, use `ConfigContextModelQuerySet` as manager, subclass `ObjectConfigContextView`/`ObjectRenderConfigView`, and mix `ConfigContextQuerySetMixin`/`RenderConfigMixin` into their API viewsets. [fg:imports:dcim.models.devices->extras.models] [fg:imports:dcim.models.devices->extras.querysets] [fg:imports:dcim.views->extras.views] [fg:imports:virtualization.views->extras.views] [fg:imports:virtualization.api.views->extras.api.mixins]

String references into extras: `DeviceRole`, `Platform` and `RenderConfigMixin` FK to `extras.ConfigTemplate`; the feature mixins in `netbox.models.features` carry GenericRelations to ImageAttachment, Bookmark, Subscription and JournalEntry; `utilities.serialization` and `utilities.tables` resolve `extras.Tag` and `extras.TableConfig` via `apps.get_model`. [fg:model_refs:dcim.models.devices:389] [fg:model_refs:dcim.models.mixins:14] [fg:model_refs:netbox.models.features:352] [fg:model_refs:netbox.models.features:451] [fg:model_refs:utilities.serialization:68] [fg:model_refs:utilities.tables:22]

`core.models.files` imports `ScriptFileSystemStorage`, so the core ManagedFile model depends on an extras storage class. [fg:imports:core.models.files->extras.storage] [code:netbox/extras/storage.py:6-14]

The import graph is therefore circular at package level (core↔extras, netbox↔extras); the code manages this with function-local imports (`from extras.models import CustomField` inside methods, `from extras.jobs import ScriptJob` inside `process_event_rules`, `import_string("extras.jobs.ScriptJob")` in `ScriptView.post`). [code:netbox/netbox/models/features.py:202-204] [code:netbox/extras/events.py:126-138] [code:netbox/extras/views.py:1350-1361]

## Where change concentrates

Total recorded commits across the slice are 3,177; the top ten modules account for 1,428 of them. `views.py` leads (278 commits, 21 authors, still changing June 2025), followed by `api/serializers` (175), `models/models.py` (175), `api/views.py` (159), `models/customfields.py` (139), `scripts.py` (131, 18 authors). [fg:churn:extras.views] [fg:churn:extras.api.serializers] [fg:churn:extras.models.models] [fg:churn:extras.api.views] [fg:churn:extras.models.customfields] [fg:churn:extras.scripts]

Custom fields are the single hottest concern: `models/customfields.py`, `api/customfields.py` (55 commits, 3 authors) and `tests/test_customfields.py` (81) together exceed 270 commits. [fg:churn:extras.models.customfields] [fg:churn:extras.api.customfields] [fg:churn:extras.tests.test_customfields]

Two files still churn despite being nearly empty: `filters.py` (89 commits since 2016, now 39 lines) and `reports.py` (55 commits, now a 35-line shim), because functionality was moved out of them rather than the files being deleted. [fg:churn:extras.filters] [fg:churn:extras.reports] [fg:modules:extras.filters] [fg:modules:extras.reports]

The event pipeline (`events.py`, `signals.py`, `webhooks.py`) is comparatively quiet—20, 55 and 41 commits—and `signals.py` has had no change since August 2024. [fg:churn:extras.events] [fg:churn:extras.signals] [fg:churn:extras.webhooks]

Recent structural migrations (0117 move ObjectChange to core, 0124 remove staging, 0128 TableConfig, 0129 fix script paths) show models leaving extras and new ones still arriving. [fg:modules:extras.migrations.0117_move_objectchange] [fg:modules:extras.migrations.0124_remove_staging] [fg:modules:extras.migrations.0128_tableconfig] [fg:modules:extras.migrations.0129_fix_script_paths]
