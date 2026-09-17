# utilities — retro-ADRs (NetBox ea4c205)

## ADR-U1: Object-level permissions are enforced by filtering querysets, not by per-object checks

**Context.** NetBox grants permissions as ObjectPermission rows with JSON constraints, and every list, detail, and API view must honour them without each view re-implementing the check. [code:netbox/utilities/permissions.py:86-114] [code:netbox/utilities/querysets.py:40-47]

**Decision.** `RestrictedQuerySet.restrict(user, action)` is the single enforcement point: superusers and exempt permissions pass through, unauthenticated or unpermitted users get `.none()`, otherwise the user's cached constraints are compiled to a `Q` and applied as `pk__in` on a fresh queryset (explicitly instead of `DISTINCT`, per the `#8715` comment). `ObjectPermissionRequiredMixin` calls `restrict()` on the view's queryset in `has_permission()`, and refuses to be used on a view without one. [code:netbox/utilities/querysets.py:48-70] [code:netbox/utilities/views.py:97-125]

**Consequences.** Every model manager must be a `RestrictedQuerySet` (or `TreeManager`, which mates it with mptt), which `netbox.models` does for its base classes; a 404 rather than 403 results when an object is filtered away, and the test harness encodes exactly that. Prefetching related objects needs `RestrictedPrefetch`, which for generic foreign keys must smuggle its parameters as a dict that `RestrictedGenericForeignKey` recognises, a workaround both files label a hack. [code:netbox/netbox/models/__init__.py:58] [code:netbox/utilities/mptt.py:13-24] [code:netbox/utilities/testing/views.py:100-117] [code:netbox/utilities/querysets.py:32-35] [code:netbox/utilities/fields.py:75-86]

## ADR-U2: Views attach to models through a registry, and URL paths are generated from it

**Context.** Object detail pages carry a variable set of tabs (changelog, journal, plugin-supplied views), and plugins must be able to add tabs to core models without editing core URLconfs. [code:netbox/utilities/views.py:285-296] [code:netbox/utilities/views.py:204-220]

**Decision.** `@register_model_view(model, name, path, detail)` records the view class in `registry['views'][app][model]`; each app's `urls.py` calls `get_model_urls()` to expand those records into `path()` entries, with names of the form `<model>_<name>`. `get_viewname()` is the inverse convention, and `model_view_tabs` renders tabs by walking the same registry and reversing those names. [code:netbox/utilities/views.py:305-322] [code:netbox/utilities/urls.py:34-50] [code:netbox/core/urls.py:9-19] [code:netbox/utilities/templatetags/tabs.py:27-59]

**Consequences.** Core apps use the decorator for every CRUD view, so the URL space is defined in `views.py` files and only mounted in `urls.py`. Anything that needs a URL (form widgets, buttons, tables, API serializers) goes through `get_viewname()`, making `utilities.views` a dependency of form fields and templatetags. Registration is import-order sensitive: views must be imported before `get_model_urls()` runs. [code:netbox/core/views.py:47-67] [fg:imports:utilities.forms.fields.dynamic->utilities.views] [fg:imports:netbox.tables.tables->utilities.views] [fg:imports:netbox.api.serializers.fields->utilities.views] [fg:imports:netbox.tests.dummy_plugin.views->utilities.views]

## ADR-U3: Related-object counts are denormalised and maintained by signals plus attribute tracking

**Context.** Device pages and tables display component counts (interfaces, ports, bays) for many devices at once; computing them per row is expensive. [code:netbox/dcim/models/devices.py:620-632] [code:netbox/utilities/counters.py:26-41]

**Decision.** `CounterCacheField` is a non-editable `BigIntegerField` declared on the parent with a string `to_model`/`to_field`; `connect_counters()` registers the mapping and connects `post_save`/`pre_delete`/`post_delete` receivers on the child model. `TrackingModelMixin` intercepts `__setattr__` on tracked FK attributes so the receiver can decrement the old parent and increment the new one. A `calculate_cached_counts` command recomputes everything from scratch. [code:netbox/utilities/fields.py:156-193] [code:netbox/utilities/counters.py:48-62] [code:netbox/utilities/tracking.py:62-78] [code:netbox/utilities/management/commands/calculate_cached_counts.py:13-34]

**Consequences.** Child models must mix in `TrackingModelMixin` and each app's `ready()` must call `connect_counters()`, or counts silently drift; `dcim` and `virtualization` do both. Bulk operations that bypass `save()`/signals leave counters stale until the command runs. Deletion of an already-deleted row is guarded by a `_previously_removed` flag set in `pre_delete`. [fg:imports:dcim.apps->utilities.counters] [fg:imports:virtualization.apps->utilities.counters] [fg:imports:dcim.models.devices->utilities.tracking] [code:netbox/utilities/counters.py:65-81]

## ADR-U4: Form select fields for model relations load options from the REST API on demand

**Context.** Foreign-key selects on NetBox forms can reference tens of thousands of objects; rendering every option server-side is not viable, and chained filtering (site → rack) is needed. [code:netbox/utilities/forms/fields/dynamic.py:56-60] [code:netbox/utilities/forms/fields/dynamic.py:69-73]

**Decision.** `DynamicModelChoiceMixin.get_bound_field()` narrows the field's queryset to the bound value (or `none()`), sets `data-url` on the `APISelect` widget to `reverse(get_viewname(model, 'list', rest_api=True))`, and encodes static and `$`-prefixed dynamic query parameters as JSON attributes the front end reads. Null selections travel as `settings.FILTERS_NULL_CHOICE_VALUE`. [code:netbox/utilities/forms/fields/dynamic.py:148-177] [code:netbox/utilities/forms/widgets/apiselect.py:51-92] [code:netbox/utilities/forms/widgets/apiselect.py:121-164] [code:netbox/utilities/forms/fields/dynamic.py:200-226]

**Consequences.** The UI depends on every referenced model having a REST list endpoint named by convention, and on the JS bundle understanding `data-dynamic-params`/`data-static-params`. `APISelect` must reset its param dicts on `__deepcopy__` because Django deep-copies widgets per form instance. This is the most-imported form module in the tree (51 inbound edges to `forms.fields`). [code:netbox/utilities/forms/widgets/apiselect.py:44-49] [fg:imports:circuits.forms.filtersets->utilities.forms.fields] [fg:imports:circuits.forms.bulk_edit->utilities.forms.fields]

## ADR-U5: Serializers, GraphQL types, tables and filtersets are found by naming convention, not registered

**Context.** Generic code (nested serializers, `GenericObjectSerializer`, table rendering, the filterset test harness) needs the companion class for an arbitrary model, including plugin models. [code:netbox/utilities/api.py:29-41] [fg:imports:netbox.api.serializers.generic->utilities.api]

**Decision.** `get_serializer_for_model`, `get_graphql_type_for_model` and `get_table_for_model` compose `<app>.<module>.<Model><Suffix>` and `import_string` it; `BaseFilterSetTests.test_missing_filters` does the same for filtersets and asserts the filter set's `Meta.model` matches. [code:netbox/utilities/api.py:43-52] [code:netbox/utilities/tables.py:31-36] [code:netbox/utilities/testing/filtersets.py:106-108]

**Consequences.** Class names and module paths are part of the contract: a serializer must live in `<app>.api.serializers` (re-exported from `serializers_/` subpackages) and be named `<Model>Serializer`. Violations surface at runtime as `SerializerNotFound`/`GraphQLTypeNotFound`, or as a silent `None` for tables. [code:netbox/utilities/api.py:35-40] [fg:imports:utilities.api->netbox.api.exceptions] [fg:imports:circuits.api.serializers_.circuits->utilities.api]

## ADR-U6: Choice enumerations are metaclass-built `ChoiceSet`s that administrators can replace or extend

**Context.** Field choices (statuses, roles, types) must serve model fields, form fields, django-filters, GraphQL enums and per-choice colours, and operators asked to add site-specific values. [code:netbox/utilities/choices.py:61-66] [code:netbox/utilities/choices.py:73-81]

**Decision.** `ChoiceSetMeta.__new__` reads `settings.FIELD_CHOICES[<app>.<key>]` to replace, or `<app>.<key>+` to extend, the static `CHOICES`; flattens optional groups; harvests a third tuple element into `colors`; and makes the class itself callable and iterable so django-filters and Django fields accept it directly. `as_enum()` derives a GraphQL-friendly `Enum`. [code:netbox/utilities/choices.py:18-58] [code:netbox/utilities/choices.py:68-81]

**Consequences.** Every app's `choices.py` subclasses it (10 inbound edges), and the `key` attribute becomes a public configuration identifier that cannot be renamed freely. Because extension mutates `CHOICES` at class-creation time, `CHOICES` must be a list when `key` is set, which the metaclass asserts. [fg:imports:dcim.choices->utilities.choices] [fg:imports:extras.choices->utilities.choices] [code:netbox/utilities/choices.py:21-24]

## ADR-U7: Change-log snapshots use Django's core serializer, not the REST API serializers

**Context.** Change logging and event payloads need a stable JSON representation of any object, including plugin models, without instantiating DRF serializers or hitting the API's nested representations. [code:netbox/utilities/serialization.py:15-19]

**Decision.** `serialize_object()` calls `django.core.serializers.serialize('json', [obj])`, takes the `fields` dict, renames `custom_field_data` to `custom_fields`, and replaces tags with their sorted names; `deserialize_object()` reverses this and hands tags back as M2M data. [code:netbox/utilities/serialization.py:28-51] [code:netbox/utilities/serialization.py:54-81]

**Consequences.** Snapshots contain raw FK integers rather than nested objects, differ from API output, and depend on `extras.utils.is_taggable` and a lazy lookup of `extras.Tag`, one of only four string references this package makes into other apps. [fg:imports:utilities.serialization->extras.utils] [fg:model_refs:utilities.serialization:68] [fg:imports:netbox.models.features->utilities.serialization] [fg:imports:extras.events->utilities.serialization]
