# core — patterns and conventions (NetBox @ ea4c205)

## Packaging and exports

- Multi-model concerns are split into one submodule per model and re-exported by a package `__init__` (or a flat `serializers.py`) using star imports: `models/__init__.py`, `tables/__init__.py`, `forms/__init__.py`, `api/serializers.py` [code:netbox/core/models/__init__.py:1-6] [code:netbox/core/tables/__init__.py:1-6] [code:netbox/core/forms/__init__.py:1-4] [code:netbox/core/api/serializers.py:1-4].
- Every leaf module declares `__all__`, so the star re-exports carry only the intended names; e.g. `data.py`, `signals.py`, `utils.py`, `graphql/types.py` [code:netbox/core/models/data.py:25-29] [code:netbox/core/signals.py:21-27] [code:netbox/core/utils.py:17-24] [code:netbox/core/graphql/types.py:11-16].
- Exception: `tables/jobs.py`, `tables/tasks.py`, `choices.py` and `plugins.py` have no `__all__`, so their star-exports expose everything public [code:netbox/core/tables/jobs.py:1-8] [code:netbox/core/tables/tasks.py:1-9].

## Base-class selection by model kind

- Models deriving from `PrimaryModel`/`NetBoxModel` get the full NetBox stack (`NetBoxModelFilterSet`, `NetBoxModelForm`, `NetBoxModelSerializer`, `NetBoxModelViewSet`, `NetBoxObjectType`), while plain `models.Model` records get the base variants (`BaseFilterSet`, `BaseModelSerializer`, `ReadOnlyModelViewSet`, `BaseObjectType`, `SavedFiltersMixin + FilterForm`). `DataSource` is the former; `Job`, `ObjectChange`, `ConfigRevision` are the latter [fg:symbols:core.filtersets:DataSourceFilterSet] [fg:symbols:core.filtersets:ObjectChangeFilterSet] [fg:symbols:core.api.serializers_.data:DataSourceSerializer] [fg:symbols:core.api.serializers_.jobs:JobSerializer] [fg:symbols:core.api.views:DataSourceViewSet] [fg:symbols:core.api.views:JobViewSet] [fg:symbols:core.forms.filtersets:JobFilterForm] [fg:symbols:core.graphql.types:ObjectChangeType].
- Exception: `DataFile` is a plain model but its filterset is a `ChangeLoggedModelFilterSet` and its serializer a `NetBoxModelSerializer` with a read-only viewset [fg:symbols:core.filtersets:DataFileFilterSet] [fg:symbols:core.api.serializers_.data:DataFileSerializer] [fg:symbols:core.api.views:DataFileViewSet].

## Views and URLs

- DB-backed model views are registered with `@register_model_view(Model, action, path=..., detail=...)` and `urls.py` includes them through `get_model_urls('core', <model>)`; both list and detail namespaces are included per model [code:netbox/core/views.py:47-48] [code:netbox/core/views.py:271-272] [code:netbox/core/urls.py:9-19] [code:netbox/core/urls.py:48-49].
- Views that operate on non-DB objects (RQ queues/tasks/workers, system, plugins) are declared with explicit `path()` entries and named views [code:netbox/core/urls.py:22-46] [code:netbox/core/urls.py:51-54].
- Staff-only screens gate with `UserPassesTestMixin.test_func` returning `request.user.is_staff`, repeated in `BaseRQView`, `SystemView` and `BasePluginView`; the API equivalent is `permission_classes = [IsAdminUser]` on `BaseRQViewSet` [code:netbox/core/views.py:343-346] [code:netbox/core/views.py:526-529] [code:netbox/core/views.py:589-593] [code:netbox/core/api/views.py:88-92].
- Table-rendering views answer HTMX requests with the bare `htmx/table.html` partial via `htmx_partial(request)`: `BackgroundTaskListView`, `WorkerListView`, `PluginListView` [code:netbox/core/views.py:377-381] [code:netbox/core/views.py:488-498] [code:netbox/core/views.py:622-626].
- Custom actions on a model are a `BaseObjectView` with `get_required_permission()` returning a custom permission string, GET redirecting to the detail page, POST doing the work (`DataSourceSyncView`, `ConfigRevisionRestoreView`) [code:netbox/core/views.py:67-91] [code:netbox/core/views.py:302-336].
- Exception: `ConfigRevisionRestoreView.post` re-checks `has_perm` by hand after the mixin already required it [code:netbox/core/views.py:328-330].

## Querysets

- List, bulk-delete and API list views defer large columns: `DataFile.objects.defer('data')` and `Job.objects.defer('data')` [code:netbox/core/views.py:137] [code:netbox/core/views.py:158] [code:netbox/core/views.py:169] [code:netbox/core/api/views.py:64].
- `ObjectChange` is always read through `valid_models()` in views and API, never `objects.all()` [code:netbox/core/views.py:202] [code:netbox/core/views.py:214] [code:netbox/core/api/views.py:83].
- Status transitions on `DataSource` bypass `save()` and use `QuerySet.update()` on the pk, in the model, the UI view, the API action, the job runner and the management command [code:netbox/core/models/data.py:172-173] [code:netbox/core/views.py:84-85] [code:netbox/core/api/views.py:55-56] [code:netbox/core/jobs.py:34] [code:netbox/core/management/commands/syncdatasource.py:42].
- Related-count annotations use `count_related(DataFile, 'source')` on the list and bulk views rather than a property on the model [code:netbox/core/views.py:49-51] [code:netbox/core/views.py:114-116].

## Registry-driven extensibility

- Pluggable sets are looked up from `netbox.registry.registry` rather than hard-coded: data backends (`registry['data_backends']` in the model, table column and forms), model features (`ObjectTypeManager.with_feature`), system jobs (`rqworker`), installed plugins (`get_local_plugins`) [code:netbox/core/models/data.py:97-110] [code:netbox/core/tables/columns.py:17-20] [code:netbox/core/forms/model_forms.py:68-70] [code:netbox/core/models/contenttypes.py:24-40] [code:netbox/core/management/commands/rqworker.py:19-26] [code:netbox/core/plugins.py:105].
- Registration is by decorator at import time: `@register_data_backend()`, `@register_search`, `@system_job(...)`, `@register(Tags.models)`; `CoreConfig.ready()` imports the modules so the decorators run [code:netbox/core/data_backends.py:29] [code:netbox/core/search.py:5] [code:netbox/core/jobs.py:40] [code:netbox/core/checks.py:10] [code:netbox/core/apps.py:24-27].
- Choice lists derived from the registry are passed as callables (`choices=get_data_backend_choices`) in forms and filtersets, so they resolve at render time; the serializer instead calls it at import (`get_data_backend_choices()`) [code:netbox/core/forms/model_forms.py:30-33] [code:netbox/core/filtersets.py:24-27] [code:netbox/core/api/serializers_/data.py:14-16].

## Choices and colours

- Status-like fields use a `ChoiceSet` whose `CHOICES` are `(value, label, colour)` triples, and the model exposes `get_<field>_color()` reading `Choices.colors`: `DataSource.status`, `Job.status`, `ObjectChange.action` [code:netbox/core/choices.py:17-23] [code:netbox/core/models/data.py:101-102] [code:netbox/core/models/jobs.py:130-131] [code:netbox/core/models/change_logging.py:141-142].
- RQ-native statuses, which are not a `ChoiceSet`, get the same treatment via `RQ_TASK_STATUSES` dataclass map and `RQJobStatusColumn` [code:netbox/core/constants.py:11-26] [code:netbox/core/tables/columns.py:26-36].

## Filtersets and filter forms

- Every filterset defines `q = CharFilter(method='search')` and a `search()` that returns the queryset unchanged when `value.strip()` is empty, then ORs `icontains` lookups [code:netbox/core/filtersets.py:52-54] [code:netbox/core/filtersets.py:70-75] [code:netbox/core/filtersets.py:128-134] [code:netbox/core/filtersets.py:184-189].
- Datetime bounds are spelled `<field>__before`/`<field>__after` as separate `DateTimeFilter`s with `lte`/`gte`, and the filter form declares the same names with `DateTimePicker` [code:netbox/core/filtersets.py:83-91] [code:netbox/core/forms/filtersets.py:89-98].
- Exception: `ObjectChangeFilterSet.time` uses `DateTimeFromToRangeFilter`, and its form uses `time_before`/`time_after` (no double underscore) [code:netbox/core/filtersets.py:142] [code:netbox/core/forms/filtersets.py:143-152].
- Filter forms open with `FieldSet('q', 'filter_id')` and group the rest into named `FieldSet`s [code:netbox/core/forms/filtersets.py:28-31] [code:netbox/core/forms/filtersets.py:71-78] [code:netbox/core/forms/filtersets.py:172-174].
- Object-type choosers are restricted to registered feature support: `ObjectType.objects.with_feature('jobs')` and `with_feature('change_logging')` [code:netbox/core/forms/filtersets.py:79-83] [code:netbox/core/forms/filtersets.py:163-167].

## GraphQL

- Types are declared with `@strawberry_django.type(model, fields/exclude, filters=..., pagination=True)` and cross-references use `Annotated[..., strawberry.lazy('core.graphql.types')]` to avoid import cycles [code:netbox/core/graphql/types.py:19-26] [code:netbox/core/graphql/types.py:29-37].
- Filter classes use `@strawberry_django.filter_type(model, lookups=True)` with `FilterLookup`/`DatetimeFilterLookup` annotations and lazy references to sibling filters [code:netbox/core/graphql/filters.py:26-39] [code:netbox/core/graphql/filters.py:59-69].

## Import-cycle handling

- Cycles between `core.models`, `core.signals` and `core.jobs` are broken by function-local imports: `DataSource.sync` imports the signals, `enqueue_sync_job` imports `SyncDataSourceJob`, `auto_sync` imports `AutoSyncRecord` [code:netbox/core/models/data.py:164] [code:netbox/core/signals.py:201] [code:netbox/core/signals.py:220].
- Optional third-party backends import their dependency inside the method (`dulwich`, `boto3`), and `DataSource.sync` converts the resulting `ModuleNotFoundError` into a `SyncError` [code:netbox/core/data_backends.py:68-69] [code:netbox/core/data_backends.py:153-155] [code:netbox/core/models/data.py:176-181].

## Model conventions

- Internal-only models set `_netbox_private = True` (`AutoSyncRecord`, `ManagedFile`) [code:netbox/core/models/data.py:378] [code:netbox/core/models/files.py:51].
- Methods with side effects are flagged `alters_data = True` for template safety (`DataSource.sync`, `ConfigRevision.activate`) [code:netbox/core/models/data.py:230] [code:netbox/core/models/config.py:62].
- Every model uses `RestrictedQuerySet.as_manager()` (or a subclass) so `.restrict(user, action)` is available [code:netbox/core/models/data.py:303] [code:netbox/core/models/jobs.py:108] [code:netbox/core/models/config.py:32] [code:netbox/core/models/change_logging.py:98].
- Uniqueness is expressed as `Meta.constraints` with `%(app_label)s_%(class)s_...` names rather than `unique_together` [code:netbox/core/models/data.py:307-312] [code:netbox/core/models/files.py:55-59] [code:netbox/core/models/data.py:381-386].
- Exception: `ManagedFile.get_absolute_url` reverses `core:managedfile`, but no such route is registered in `core/urls.py` [code:netbox/core/models/files.py:67-68] [code:netbox/core/urls.py:6-55].

## RQ access

- Every raw-RQ helper fetches the job through `QUEUES_LIST[0]`'s connection on the stated assumption that all queues share one Redis connection, then resolves the real queue via `QUEUES_MAP[job.origin]`; the same shape appears in `utils.py` four times and in the views [code:netbox/core/utils.py:76-91] [code:netbox/core/utils.py:142-155] [code:netbox/core/views.py:392-401] [code:netbox/core/api/views.py:160-163].
- UI views and API actions share those helpers rather than each talking to RQ [code:netbox/core/views.py:23] [code:netbox/core/api/views.py:16] [code:netbox/core/views.py:436] [code:netbox/core/api/views.py:206].

## Tests

- View, API and filterset tests are built on the shared `utilities.testing` case mixins (`ViewTestCases.PrimaryObjectViewTestCase`, `APIViewTestCases.APIViewTestCase`, `ChangeLoggedFilterSetTests`) [fg:symbols:core.tests.test_views:DataSourceTestCase] [fg:symbols:core.tests.test_api:DataSourceTest] [fg:symbols:core.tests.test_filtersets:DataSourceTestCase].
- Change logging is tested against `dcim` models, not core's own, because the receivers are global [fg:imports:core.tests.test_changelog->dcim.models] [code:netbox/core/tests/test_changelog.py:18-19].

## Bulk-edit anomaly

- `DataSourceBulkEditForm.nullable_fields` repeats `'description'` and `'parameters'` and is missing a comma between `'ignore_rules'` and `'comments'`, so the tuple contains the concatenated string `'ignore_rulescomments'` and neither field is nullable by name [code:netbox/core/forms/bulk_edit.py:53-55].
