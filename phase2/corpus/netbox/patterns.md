# netbox (core package) — patterns and conventions

## Module and package shape

- Every non-trivial module declares `__all__` near the top, and package `__init__` files re-export submodules with star imports, so consumers write `from netbox.views import generic` or `from netbox.tables import columns` rather than deep paths. 44 non-test modules follow this. [code:netbox/netbox/views/generic/__init__.py:1-3] [code:netbox/netbox/tables/__init__.py:1-2] [code:netbox/netbox/models/__init__.py:10-22]
- Cross-app model imports that would form a cycle are done inside the method that needs them, never at module scope; the same module imports `core.choices` at the top but `core.models.ObjectChange` inside `to_objectchange()`. [code:netbox/netbox/models/features.py:13-23] [code:netbox/netbox/models/features.py:96-97] [code:netbox/netbox/models/features.py:543-546]
- Declarative data is expressed with `@dataclass` (menu items, event types, table action items, GraphQL filter mixins) rather than dicts or ad-hoc classes. [code:netbox/netbox/navigation/__init__.py:19-50] [code:netbox/netbox/events.py:38-53] [code:netbox/netbox/graphql/filter_mixins.py:43-45]
- User-facing strings and field `verbose_name`s go through `gettext_lazy as _`; log messages and exceptions aimed at operators do not. [code:netbox/netbox/models/__init__.py:110-122] [code:netbox/netbox/forms/base.py:85-91] [code:netbox/netbox/config/parameters.py:17-30]
- Loggers are named `netbox.<area>.<ClassName>` and fetched inside the handler that uses them. [code:netbox/netbox/views/generic/object_views.py:268] [code:netbox/netbox/api/viewsets/__init__.py:137] [code:netbox/netbox/middleware.py:119]

## Feature composition

- Model capabilities are abstract `models.Model` mixins with `Meta.abstract = True`; base classes are built by stacking them, and `NetBoxFeatureSet` is the canonical bundle. [code:netbox/netbox/models/features.py:49-67] [code:netbox/netbox/models/__init__.py:25-39] [code:netbox/netbox/models/__init__.py:180-209]
- The same mixin idea is mirrored per layer: `TaggableModelSerializer`/`CustomFieldModelSerializer` compose `NetBoxModelSerializer`; `CustomFieldsMixin`/`TagsMixin` compose `NetBoxModelForm`; `ChangelogMixin`/`CustomFieldsMixin`/`TagsMixin` compose `NetBoxObjectType`; DRF `mixins.*` compose `NetBoxModelViewSet`. [code:netbox/netbox/api/serializers/__init__.py:13-17] [code:netbox/netbox/forms/base.py:24] [code:netbox/netbox/graphql/types.py:67-77] [code:netbox/netbox/api/viewsets/__init__.py:99-111]
- Feature presence is detected with `issubclass(model, Mixin)` or `hasattr(obj, 'snapshot')`/`hasattr(model, 'custom_fields')`, never with flags. [code:netbox/netbox/models/features.py:661-691] [code:netbox/netbox/api/viewsets/mixins.py:28-31] [code:netbox/netbox/views/generic/object_views.py:273-274]
- Custom fields are injected dynamically under a `cf_` prefix in every layer: form fields, filterset filters, table columns and search cache entries. [code:netbox/netbox/forms/mixins.py:51-63] [code:netbox/netbox/filtersets.py:297-315] [code:netbox/netbox/tables/tables.py:243-250] [code:netbox/netbox/search/__init__.py:118-129]
- Mutating model methods are marked `alters_data = True` so Django templates cannot invoke them. [code:netbox/netbox/models/features.py:79-89] [code:netbox/netbox/models/features.py:591-602] [code:netbox/netbox/models/deletion.py:66-81]

## Registration through the registry

- Extension points are populated by calling into the single `registry` object from decorators or `register_*` helpers: `register_search`, `register_data_backend`, `register_request_processor`, `system_job`, `EventType.register`, `denormalized.register`, `register_models` and the plugin helpers. [code:netbox/netbox/search/__init__.py:143-151] [code:netbox/netbox/utils.py:19-36] [code:netbox/netbox/jobs.py:21-34] [code:netbox/netbox/events.py:58-61] [code:netbox/netbox/plugins/registration.py:18-44]
- Modules that own a registry store initialise its sub-keys at import time (`registry['model_features'].update(...)`, `registry['plugins'].update(...)`). [code:netbox/netbox/models/features.py:636-638] [code:netbox/netbox/plugins/__init__.py:18-26]
- Registration happens in `AppConfig.ready()`, both for core apps and for plugins, which is when models are importable. [code:netbox/netbox/plugins/__init__.py:100-134] [code:netbox/dcim/apps.py:10-17] [code:netbox/netbox/tests/dummy_plugin/__init__.py:24-27]

## Convention-derived names

- Templates, view names, docs URLs and form/filterset classes are resolved from `app_label` and `model_name` rather than declared: `f'{app_label}/{model_name}.html'`, `get_viewname(model, action)`, `f'{app_label}.forms.{Model}FilterForm'`. [code:netbox/netbox/views/generic/object_views.py:53-61] [code:netbox/netbox/views/generic/feature_views.py:74-77] [code:netbox/netbox/views/htmx.py:45-57] [code:netbox/netbox/models/__init__.py:41-46]
- Menu entries follow the same rule: `get_model_item(app, model, label)` derives the list/add/import URL names and view/add permissions from the two labels. [code:netbox/netbox/navigation/__init__.py:62-93] [code:netbox/netbox/navigation/menu.py:10-22]
- Generic views take their model from `queryset.model` and never declare it separately; `template_name`, `form`, `table`, `filterset`, `filterset_form` are class attributes overridden by subclasses. [code:netbox/netbox/views/generic/base.py:13-40] [code:netbox/netbox/views/generic/bulk_views.py:50-65] [code:netbox/netbox/views/generic/object_views.py:170-190]

## Permission enforcement

- Required permission is computed as `get_permission_for_model(self.queryset.model, action)` in a `get_required_permission()` override; the API maps HTTP methods to actions with `HTTP_ACTIONS` and `TokenPermissions.perms_map`. [code:netbox/netbox/views/generic/object_views.py:50-51] [code:netbox/netbox/views/generic/bulk_views.py:552-553] [code:netbox/netbox/api/viewsets/__init__.py:23-31] [code:netbox/netbox/api/authentication.py:86-95]
- Reads are restricted by `queryset.restrict(user, action)` in views, viewsets, feature views and GraphQL types. [code:netbox/netbox/api/viewsets/__init__.py:40-46] [code:netbox/netbox/views/generic/feature_views.py:53-57] [code:netbox/netbox/graphql/types.py:28-34] [code:netbox/netbox/views/htmx.py:23]
- Writes run inside `transaction.atomic(using=router.db_for_write(model))`, and after saving, the view checks the object is still matched by its restricted queryset, raising `PermissionsViolation` (UI) or `ObjectDoesNotExist`→`PermissionDenied` (API) to roll back. [code:netbox/netbox/views/generic/object_views.py:284-291] [code:netbox/netbox/views/generic/bulk_views.py:502-509] [code:netbox/netbox/api/viewsets/__init__.py:171-177] [code:netbox/netbox/api/viewsets/mixins.py:167-180]

## Change logging and events

- Before any mutation of an existing object the code calls `obj.snapshot()` (guarded by `hasattr`) so the changelog can record pre-change data; this appears in UI edit/delete, bulk edit/rename/delete/import, and API update/destroy/bulk paths. [code:netbox/netbox/views/generic/object_views.py:459-461] [code:netbox/netbox/views/generic/bulk_views.py:593-596] [code:netbox/netbox/api/viewsets/__init__.py:115-123] [code:netbox/netbox/api/viewsets/mixins.py:115-127]
- When a write is aborted (`AbortRequest`, `PermissionsViolation`, `ValidationError`), handlers send `clear_events.send(sender=self)` so queued webhooks/event-rule events for the rolled-back transaction are discarded. [code:netbox/netbox/views/generic/object_views.py:336-339] [code:netbox/netbox/views/generic/bulk_views.py:520-526] [code:netbox/netbox/views/generic/bulk_views.py:699-706]
- Handlers catch `AbortRequest`/`PermissionsViolation` and surface `e.message` as a non-field form error (UI) or a 400/409 `detail` response (API). [code:netbox/netbox/views/generic/object_views.py:594-597] [code:netbox/netbox/api/viewsets/__init__.py:136-162]

## HTMX and request handling

- Views branch on `htmx_partial(request)` to return a fragment template (`htmx/table.html`, `htmx/form.html`, `htmx/delete_form.html`) and use `HX-Location`/`HX-Redirect` headers instead of HTTP redirects when `request.htmx` is set. [code:netbox/netbox/views/generic/object_views.py:146-152] [code:netbox/netbox/views/generic/object_views.py:328-332] [code:netbox/netbox/views/generic/bulk_views.py:183-194] [code:netbox/netbox/views/generic/object_views.py:427-438]
- Runtime configuration is read through `get_config().PARAM` (thread-local, cleared by `CoreMiddleware` after every request), while `settings.PARAM` is reserved for static values. [code:netbox/netbox/config/__init__.py:23-39] [code:netbox/netbox/middleware.py:67-68] [code:netbox/netbox/api/pagination.py:13-14] [code:netbox/netbox/models/features.py:84-88]
- Redirect targets derived from request data pass through `safe_for_redirect()` before use. [code:netbox/netbox/views/generic/object_views.py:317-324] [code:netbox/netbox/views/generic/bulk_views.py:122-128]

## Exceptions to the patterns

- `ObjectChangeLogView`, `ObjectJournalView` and siblings do not extend `BaseObjectView`; they are plain `View`s receiving `model` as a URL kwarg and registered by string path from `register_models()`. [code:netbox/netbox/views/generic/feature_views.py:34-57] [code:netbox/netbox/models/features.py:672-692]
- `ChangeLoggedModel` deliberately omits most of `NetBoxFeatureSet`, and `NestedGroupModel` uses `TreeManager()` where the other bases use `RestrictedQuerySet.as_manager()`. [code:netbox/netbox/models/__init__.py:53-61] [code:netbox/netbox/models/__init__.py:128-159]
- `SyncedDataMixin.clean()` mutates the instance (assigns source/path, calls `sync()`) and is marked `alters_data`, unlike every other `clean()` in the package. [code:netbox/netbox/models/features.py:528-541]
- `ComponentCreateView.alter_object(instance, request)` has a different signature from `ObjectEditView.alter_object(obj, request, url_args, url_kwargs)`. [code:netbox/netbox/views/generic/object_views.py:201-212] [code:netbox/netbox/views/generic/object_views.py:514-515]
- `BulkEditView.post()` hard-codes `device`, `device_type` and `virtual_machine` as the only GET parameters passed to the form, with a TODO acknowledging it. [code:netbox/netbox/views/generic/bulk_views.py:665-673]
- `SequentialBulkCreatesMixin` is opt-in rather than part of `NetBoxModelViewSet`; `MPTTLockedMixin` requires a hand-maintained key in `ADVISORY_LOCK_KEYS`. [code:netbox/netbox/api/viewsets/mixins.py:53-74] [code:netbox/netbox/api/viewsets/__init__.py:214-230] [code:netbox/netbox/constants.py:10-29]
- `ValidatedModelSerializer` disables DRF's unique-together validation and reruns `full_clean()` on a model instance instead, citing a DRF bug. [code:netbox/netbox/api/serializers/base.py:74-113]
- The test fixture's `DummyModel` is a plain `models.Model`, not a `NetBoxModel`, so plugin tests exercise both registered-feature and feature-less models. [code:netbox/netbox/tests/dummy_plugin/models.py:6-19]
