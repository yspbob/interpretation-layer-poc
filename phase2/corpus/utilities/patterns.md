# utilities — patterns and conventions (NetBox ea4c205)

## Public surface is declared with `__all__`; subpackages re-export by star-import

Nearly every module opens with an `__all__` tuple listing its exported names, sorted alphabetically, and the subpackage `__init__` files contain nothing but `from .x import *` lines. Consumers therefore import from `utilities.forms`, `utilities.forms.fields`, `utilities.forms.widgets` and `utilities.testing`, not from the leaf modules, and the inbound edge counts reflect that (51 edges to `forms.fields`, 44 to `testing`, 38 to `forms`). [code:netbox/utilities/views.py:16-25] [code:netbox/utilities/api.py:18-26] [code:netbox/utilities/forms/__init__.py:1-4] [code:netbox/utilities/forms/fields/__init__.py:1-6] [code:netbox/utilities/testing/__init__.py:1-5] [fg:imports:circuits.forms.model_forms->utilities.forms.fields]

Exceptions: `counters.py`, `tracking.py`, `forms/bulk_import.py`, `release.py`, `socks.py`, `templatetags/plugins.py` and the management command define no `__all__`. [code:netbox/utilities/counters.py:1-7] [code:netbox/utilities/tracking.py:1-4] [code:netbox/utilities/forms/bulk_import.py:1-13] [code:netbox/utilities/release.py:1-12]

## Resolution by naming convention, via `import_string`

Rather than registries or explicit maps, several helpers locate a class by composing a dotted path from the model's `app_label` and class name and calling `import_string`: serializers at `<app>.api.serializers.<Model>Serializer`, GraphQL types at `<app>.graphql.types.<Model>Type`, tables at `<app>.tables.<Model>Table`, and (in the test harness) filtersets at `<app>.filtersets.<Model>FilterSet`. A missing class raises a domain exception (`SerializerNotFound`, `GraphQLTypeNotFound`) or returns `None` (tables). [code:netbox/utilities/api.py:29-52] [code:netbox/utilities/tables.py:31-36] [code:netbox/utilities/testing/filtersets.py:102-108]

The same idea governs URL names: `get_viewname()` produces `<app>:<model>_<action>` for UI views and `<app>-api:<model>-<action>` for REST views, with a `plugins:`/`plugins-api:` prefix when the model's app config is a `PluginConfig`. The test harness derives URLs the same way independently. [code:netbox/utilities/views.py:256-282] [code:netbox/utilities/testing/views.py:33-53] [code:netbox/utilities/testing/api.py:53-62]

## Extension through `netbox.registry`, written by decorators/functions and read by templatetags and URLconfs

Write side: `register_model_view()` appends to `registry['views'][app][model]`; `register_table_column()` writes to `registry['tables'][table]`; `connect_counters()` writes to `registry['counter_fields'][model]`. Read side: `get_model_urls()` and the `model_view_tabs` tag consume `registry['views']`; `TrackingModelMixin.__setattr__` and the management command consume `registry['counter_fields']`; plugin tags consume `registry['plugins']['template_extensions']`. [code:netbox/utilities/views.py:305-322] [code:netbox/utilities/tables.py:63-78] [code:netbox/utilities/counters.py:99-104] [code:netbox/utilities/urls.py:24-32] [code:netbox/utilities/templatetags/tabs.py:27-36] [code:netbox/utilities/tracking.py:62-73] [code:netbox/utilities/templatetags/plugins.py:25-28]

## Lazy model and module resolution to avoid import cycles

Where a utility needs a concrete model from `core`, `extras` or `users`, it resolves it at call time with `apps.get_model()` or a function-local import rather than a module-level import: `TableConfig` in `tables.py`, `DataFile` in `jinja2.py`, `User` and `ObjectType` in `permissions.py`, `Tag` in `serialization.py`, `CustomValidator` in `json.py`. `socks.py` does the same for the optional `python_socks` dependency. [code:netbox/utilities/tables.py:22] [code:netbox/utilities/jinja2.py:23] [code:netbox/utilities/permissions.py:55] [code:netbox/utilities/permissions.py:96] [code:netbox/utilities/serialization.py:68] [code:netbox/utilities/json.py:26] [code:netbox/utilities/socks.py:26-33]

Exception: `tables.py`, `templatetags/buttons.py`, `templatetags/helpers.py` and `testing/*` import `core.models.ObjectType` at module level, and `buttons.py` imports `extras.models` at module level. [fg:imports:utilities.tables->core.models] [fg:imports:utilities.templatetags.buttons->extras.models] [code:netbox/utilities/templatetags/buttons.py:5-7]

## Dynamic configuration is read through `get_config()` at call time; static settings through `django.conf.settings`

Values that administrators can change at runtime (`PAGINATE_COUNT`, `MAX_PAGE_SIZE`, `ALLOWED_URL_SCHEMES`, `JINJA2_FILTERS`, `QUEUE_MAPPINGS`, `RQ_RETRY_*`) are fetched inside the function body via `netbox.config.get_config()`; `EnhancedURLValidator` even defers its `schemes` attribute until first call with a comment explaining why. Values fixed in `configuration.py` (`LOGIN_REQUIRED`, `EXEMPT_VIEW_PERMISSIONS`, `FIELD_CHOICES`, `HTTP_PROXIES`, `BASE_PATH`) are read from `settings`. [code:netbox/utilities/paginator.py:17-33] [code:netbox/utilities/validators.py:42-46] [code:netbox/utilities/rqworker.py:14-36] [code:netbox/utilities/jinja2.py:68-69] [code:netbox/utilities/views.py:36-39] [code:netbox/utilities/permissions.py:65-83] [code:netbox/utilities/choices.py:21-33]

## Permission names are always `<app_label>.<action>_<model_name>`

`get_permission_for_model()` builds them, `resolve_permission()` parses them, `permission_is_exempt()` and `resolve_permission_type()` build on the parser, `RestrictedQuerySet.restrict()` and the view mixins pass them through, the `perms` templatetags and the test harness's `add_permissions()` accept them. Proxy models are resolved to their concrete model first. [code:netbox/utilities/permissions.py:17-45] [code:netbox/utilities/querysets.py:48-57] [code:netbox/utilities/views.py:97-110] [code:netbox/utilities/templatetags/perms.py:17-30] [code:netbox/utilities/testing/base.py:43-52]

## Multi-value filters are generated by a factory and annotated for OpenAPI

`multivalue_field_factory()` wraps a Django form field class so `to_python`/`validate`/`run_validators` operate per-value; each `MultiValue*Filter` is a two-line `MultipleChoiceFilter` subclass using it, decorated with `@extend_schema_field` so drf-spectacular reports a scalar type instead of a choice list. [code:netbox/utilities/filters.py:26-51] [code:netbox/utilities/filters.py:58-90] [code:netbox/utilities/filters.py:103-120]

## Thin subclasses of Django/DRF/library classes with one changed attribute

Widgets override only `template_name` or `option_template_name` (`ClearableFileInput`, `MarkdownWidget`, `ColorSelect`, `SelectWithPK`, `APISelect`); `TreeQuerySet`/`TreeManager` are empty multiple-inheritance mates; `EmptyGroupByJSONBAgg` flips `contains_aggregate`; `CustomFieldJSONEncoder` and `ConfigJSONEncoder` override `default()` only. [code:netbox/utilities/forms/widgets/misc.py:13-24] [code:netbox/utilities/forms/widgets/select.py:30-39] [code:netbox/utilities/forms/widgets/select.py:61-65] [code:netbox/utilities/mptt.py:13-24] [code:netbox/utilities/query_functions.py:18-24] [code:netbox/utilities/json.py:11-31]

## Sentinel and token strings shared with the front end

`settings.FILTERS_NULL_CHOICE_VALUE` is the agreed marker for "null" in filters and dynamic fields (`NullableCharFieldFilter`, `DynamicModelChoiceField.clean`, `DynamicModelMultipleChoiceField.clean`, widget choices). A leading `$` marks a value to be resolved client-side or from the form: `APISelect._process_query_param` (dynamic query params), `initial_params` (`lstrip('$')`), and `quick_add_params` (`'$pk'`). [code:netbox/utilities/filters.py:139-143] [code:netbox/utilities/forms/fields/dynamic.py:167-172] [code:netbox/utilities/forms/fields/dynamic.py:200-226] [code:netbox/utilities/forms/widgets/apiselect.py:68-83] [code:netbox/utilities/forms/fields/dynamic.py:139-146] [code:netbox/utilities/forms/fields/dynamic.py:185-191]

## Custom model fields control their own migration serialization

`NaturalOrderingField.deconstruct()` returns a hard-coded path and re-injects `naturalize_function`; `CounterCacheField.deconstruct()` re-adds `to_model`/`to_field`; `migration.custom_deconstruct()` strips `choices`, `help_text`, `verbose_name` and any `ConfigItem` default so cosmetic changes do not generate migrations. [code:netbox/utilities/fields.py:62-70] [code:netbox/utilities/fields.py:189-193] [code:netbox/utilities/migration.py:10-34]

## Test-case building blocks are nested inside holder classes

`ViewTestCases` and `APIViewTestCases` are plain classes whose members are `TestCase` subclasses; the docstring states this is to stop unittest discovering them directly, so app tests compose the ones they need. Anonymous-access tests uniformly use `@override_settings(EXEMPT_VIEW_PERMISSIONS=['*'], LOGIN_REQUIRED=False)` and branch on `EXEMPT_EXCLUDE_MODELS`. [code:netbox/utilities/testing/views.py:56-76] [code:netbox/utilities/testing/api.py:65-81] [code:netbox/utilities/testing/api.py:128-140]

## User-facing strings are wrapped in `_()`

Error messages, labels and help text go through `gettext_lazy` as `_` at module level in views, fields, validators, mixins and CSV fields. Form modules (`forms/forms.py`, `forms/bulk_import.py`, `forms/utils.py`, `testing/views.py`) import the non-lazy `gettext` instead. [code:netbox/utilities/views.py:8] [code:netbox/utilities/fields.py:10] [code:netbox/utilities/forms/mixins.py:6] [code:netbox/utilities/forms/forms.py:4] [code:netbox/utilities/forms/bulk_import.py:7] [code:netbox/utilities/forms/utils.py:5]

## Files are sectioned with `#\n# Title\n#` banner comments

Modules with more than one concern separate them with three-line banner comments: "View Mixins"/"Utility functions" in `views.py`, "Signal handlers"/"Registration" in `counters.py`, "Fake request object"/"Utility functions" in `request.py`, "Filters" in `filters.py`, "Choice fields"/"Model choice fields" in `dynamic.py`. [code:netbox/utilities/views.py:28-30] [code:netbox/utilities/views.py:252-254] [code:netbox/utilities/counters.py:44-46] [code:netbox/utilities/request.py:17-19] [code:netbox/utilities/forms/fields/dynamic.py:18-20] [code:netbox/utilities/forms/fields/dynamic.py:52-54]
