# tenancy — patterns and conventions (NetBox @ ea4c205)

## P1. Every model gets the same seven views, declared with `register_model_view` and routed by `get_model_urls`

Each model in `views.py` has List, detail, Edit (registered twice: `add` with `detail=False` and `edit`), Delete, BulkImport, BulkEdit and BulkDelete classes, all thin subclasses of `netbox.views.generic` with `queryset`, `filterset`, `filterset_form`, `table`, `form`/`model_form` attributes and no request handling of their own. [code:netbox/tenancy/views.py:15-50] [code:netbox/tenancy/views.py:53-84] [code:netbox/tenancy/views.py:281-340]

`urls.py` contains no view references at all: each model contributes exactly two `path()` lines, one non-detail and one `<int:pk>/`, both expanded by `get_model_urls('tenancy', <model_name>)`. [code:netbox/tenancy/urls.py:9-25] [fg:imports:tenancy.urls->utilities.urls]

*Exception:* ContactAssignment has no detail view; its list view restricts `actions` to export and the three bulk operations, and its Edit view overrides `alter_object()` to bind the target object from `?object_type=&object_id=` query parameters. [code:netbox/tenancy/views.py:346-377]

## P2. Every model gets the same REST triple: viewset, serializer, filterset, wired by `NetBoxRouter`

Each viewset in `api/views.py` is `NetBoxModelViewSet` with only `queryset`, `serializer_class`, `filterset_class`. [code:netbox/tenancy/api/views.py:33-36] [code:netbox/tenancy/api/views.py:61-70]

Serializers declare a full `fields` list and a `brief_fields` tuple, and nest related objects with `nested=True` instances of sibling serializers. [code:netbox/tenancy/api/serializers_/tenants.py:27-50] [code:netbox/tenancy/api/serializers_/contacts.py:63-78]

*Exception:* the two MPTT group viewsets add `MPTTLockedMixin` (advisory lock on create/update) and take a cumulative `add_related_count` queryset; the parent field uses a dedicated `WritableNestedSerializer` in `serializers_/nested.py` rather than the full serializer. [code:netbox/tenancy/api/views.py:21-30] [code:netbox/tenancy/api/views.py:43-52] [code:netbox/tenancy/api/serializers_/nested.py:13-34] [code:netbox/netbox/api/viewsets/__init__.py:214-226]

## P3. Group models are MPTT `NestedGroupModel`s and are filtered/counted the same way

TenantGroup and ContactGroup both subclass `NestedGroupModel`; their filtersets both expose `parent_id`/`parent` (direct) and `ancestor_id`/`ancestor` (`TreeNodeMultipleChoiceFilter` on `parent`, `lookup_expr='in'`). [fg:symbols:tenancy.models.tenants:TenantGroup] [fg:symbols:tenancy.models.contacts:ContactGroup] [code:netbox/tenancy/filtersets.py:25-48] [code:netbox/tenancy/filtersets.py:171-194]

List, BulkEdit and BulkDelete views and the API viewset for each group compute `tenant_count` / `contact_count` with `add_related_count(..., cumulative=True)`, and the detail view passes `get_descendants(include_self=True)` to `get_related_models`, so counts and related lists include children. [code:netbox/tenancy/views.py:17-38] [code:netbox/tenancy/views.py:147-174] [code:netbox/tenancy/api/views.py:22-28]

Tables render group names with `columns.MPTTColumn` and the count with `LinkedCountColumn` pointing at the child list filtered by `group_id`. [code:netbox/tenancy/tables/tenants.py:15-23] [code:netbox/tenancy/tables/contacts.py:18-26]

*Exception:* the two groups diverge on uniqueness — TenantGroup re-declares `name` and `slug` as globally `unique=True`; ContactGroup uses a `(parent, name)` constraint. [code:netbox/tenancy/models/tenants.py:18-28] [code:netbox/tenancy/models/contacts.py:24-31]

## P4. Filters come in `<name>_id` / `<name>` pairs; tree filters use `TreeNodeMultipleChoiceFilter`

Every FK filter is declared twice: `*_id` as `ModelMultipleChoiceFilter` on the pk and the bare name with `to_field_name='slug'`. [code:netbox/tenancy/filtersets.py:107-133] [code:netbox/tenancy/filtersets.py:248-257]

Where the target is an MPTT group, both halves are `TreeNodeMultipleChoiceFilter` with `lookup_expr='in'`, so a filter on a group matches its whole subtree (`group_id` on Tenant and Contact, `tenant_group_id` in TenancyFilterSet, `contact_group` in ContactModelFilterSet). [code:netbox/tenancy/filtersets.py:68-80] [code:netbox/tenancy/filtersets.py:202-214] [code:netbox/tenancy/filtersets.py:235-247] [code:netbox/tenancy/filtersets.py:159-164]

Model filtersets define `search()` as an OR of `icontains` on the model's text fields and return the queryset unchanged when `value.strip()` is empty. [code:netbox/tenancy/filtersets.py:86-98] [code:netbox/tenancy/filtersets.py:220-228] [code:netbox/tenancy/filtersets.py:139-145]

## P5. Cross-app "tenancy support" is delivered as importable mixins, one per layer

The subsystem exports a mixin for each layer and consumers compose them into their own classes: `TenancyForm` (model form fields `tenant_group` + `tenant`, chained with `initial_params`/`query_params`), `TenancyFilterForm` (filter-form fields), `TenancyFilterSet` (filterset fields), `TenancyColumnsMixin` (table columns), `TenancyFilterMixin` (GraphQL filter fields). [code:netbox/tenancy/forms/forms.py:14-50] [code:netbox/tenancy/filtersets.py:231-257] [code:netbox/tenancy/tables/columns.py:44-50] [code:netbox/tenancy/graphql/filter_mixins.py:27-38]

The contacts feature has the same shape: `ContactModelFilterForm`, `ContactModelFilterSet`, `ContactsColumnMixin`, `ContactFilterMixin`, and the GraphQL `ContactsMixin` living in extras. [code:netbox/tenancy/forms/forms.py:53-68] [code:netbox/tenancy/filtersets.py:148-164] [code:netbox/tenancy/tables/columns.py:53-58] [code:netbox/tenancy/graphql/filter_mixins.py:20-24] [code:netbox/extras/graphql/mixins.py:59-61]

Consumers inherit these before or after the NetBox base class, e.g. `SiteForm(TenancyForm, NetBoxModelForm)`, `SiteFilterSet(NetBoxModelFilterSet, TenancyFilterSet, ContactModelFilterSet)`, `SiteTable(TenancyColumnsMixin, ContactsColumnMixin, NetBoxTable)`, `CableFilter(PrimaryModelFilterMixin, TenancyFilterMixin)`. [code:netbox/dcim/forms/model_forms.py:117] [code:netbox/dcim/filtersets.py:146] [code:netbox/dcim/tables/sites.py:82] [code:netbox/dcim/graphql/filters.py:94]

The subsystem uses its own mixins too: `TenantFilterSet` inherits `ContactModelFilterSet`, `TenantFilterForm` inherits `ContactModelFilterForm`, and `TenantTable` inherits `ContactsColumnMixin`. [code:netbox/tenancy/filtersets.py:201] [code:netbox/tenancy/forms/filtersets.py:38-43] [code:netbox/tenancy/tables/tenants.py:40]

*Exception:* the mixins are plain `django_filters.FilterSet` / `forms.Form` / `tables.Table`, not NetBox base classes, so they contribute fields only and rely on the consumer's MRO for `Meta`, `model` and search behaviour. [fg:symbols:tenancy.filtersets:TenancyFilterSet] [fg:symbols:tenancy.forms.forms:TenancyFilterForm] [fg:symbols:tenancy.tables.columns:TenancyColumnsMixin]

## P6. "Supports contacts" is a registry feature, not an import

A model opts in by mixing in `netbox.models.features.ContactsMixin`; `register_models()` records it under `registry['model_features']['contacts']` and auto-registers `ObjectContactsView` as a `contacts` tab. [code:netbox/netbox/models/features.py:362-373] [code:netbox/netbox/models/features.py:641-676] [code:netbox/netbox/views/generic/feature_views.py:255-274]

Tenancy code discovers eligible object types at runtime through `ObjectType.objects.with_feature('contacts')` — in `ContactAssignment.clean()` and in the assignment filter form — rather than enumerating models. [code:netbox/tenancy/models/contacts.py:150-157] [code:netbox/tenancy/forms/filtersets.py:89-93] [code:netbox/core/models/contenttypes.py:24-40]

*Exception:* the CSV import form's `object_type` field is scoped to `ContentType.objects.all()`, leaving enforcement to the model. [code:netbox/tenancy/forms/bulk_import.py:93-96]

## P7. GraphQL avoids import cycles with `strawberry.lazy` and `TYPE_CHECKING`

Every cross-module type or filter annotation is `Annotated['Name', strawberry.lazy('<module>')]`, and the real imports sit under `if TYPE_CHECKING:` so no peer app is imported at runtime. [code:netbox/tenancy/graphql/types.py:12-38] [code:netbox/tenancy/graphql/types.py:60-85] [code:netbox/tenancy/graphql/filters.py:18-47] [code:netbox/tenancy/graphql/filter_mixins.py:10-12]

Tenancy applies the same trick to itself: `ContactAssignmentsMixin` and `TenantGroupType.parent` lazily reference `tenancy.graphql.types`. [code:netbox/tenancy/graphql/mixins.py:10-12] [code:netbox/tenancy/graphql/types.py:94-98]

## P8. Form field conventions

Model forms declare a `fieldsets` tuple of `FieldSet(...)`, use `DynamicModelChoiceField` / `DynamicModelMultipleChoiceField` for FKs and M2Ms, `SlugField()` for slugs and `CommentField()` for comments. [code:netbox/tenancy/forms/model_forms.py:23-40] [code:netbox/tenancy/forms/model_forms.py:97-119]

Dependent selectors chain with `initial_params` (parent pre-filled from child) and `query_params` (child filtered by parent): `tenant_group`→`tenant` in TenancyForm and `group`→`contact` in ContactAssignmentForm. [code:netbox/tenancy/forms/forms.py:14-32] [code:netbox/tenancy/forms/model_forms.py:122-141]

Bulk-edit forms set `model`, `fieldsets` and `nullable_fields`; import forms use `CSVModelChoiceField(to_field_name='name')`. [code:netbox/tenancy/forms/bulk_edit.py:42-53] [code:netbox/tenancy/forms/bulk_edit.py:147-168] [code:netbox/tenancy/forms/bulk_import.py:22-49]

*Exception:* M2M bulk editing is done with paired `add_groups`/`remove_groups` fields, and the view's `post_save_operations()` applies them; this is the only bulk-edit view in the app with custom logic. [code:netbox/tenancy/forms/bulk_edit.py:94-104] [code:netbox/tenancy/views.py:323-330]

## P9. Packages re-export with star imports and explicit `__all__`

`models`, `forms`, `tables` and `api/serializers` are packages (or shims) whose `__init__` does only `from .x import *`; each submodule guards the surface with `__all__`. [code:netbox/tenancy/models/__init__.py:1-2] [code:netbox/tenancy/forms/__init__.py:1-5] [code:netbox/tenancy/api/serializers.py:1-2] [code:netbox/tenancy/filtersets.py:9-18]

Consequently every inbound import from other apps targets the package name (`tenancy.models`, `tenancy.forms`, `tenancy.tables`), except serializers, which are imported from `tenancy.api.serializers_.tenants` directly. [fg:imports:dcim.forms.bulk_edit->tenancy.models] [fg:imports:ipam.tables.ip->tenancy.tables] [fg:imports:ipam.api.serializers_.ip->tenancy.api.serializers_.tenants]

## P10. Tests are one class per model built on shared base cases

`test_api.py` uses `APIViewTestCases.APIViewTestCase` with class-level `brief_fields` and `bulk_update_data` and `cls.create_data` set in `setUpTestData`; `test_views.py` uses `ViewTestCases.OrganizationalObjectViewTestCase` / `PrimaryObjectViewTestCase`; `test_filtersets.py` uses `TestCase, ChangeLoggedFilterSetTests` with one `test_<filter>` per filter. [code:netbox/tenancy/tests/test_api.py:19-44] [code:netbox/tenancy/tests/test_views.py:10-14] [code:netbox/tenancy/tests/test_filtersets.py:10-15] [code:netbox/tenancy/tests/test_filtersets.py:357-373]

*Exception:* ContactAssignment's view test composes the individual `ViewTestCases` mixins by hand (omitting the detail-view and bulk-import cases), and all three ContactAssignment tests create `dcim.Site` rows as assignment targets. [code:netbox/tenancy/tests/test_views.py:240-259] [code:netbox/tenancy/tests/test_api.py:223-238] [fg:imports:tenancy.tests.test_views->dcim.models]

## P11. Migrations that change shape carry data moves and change-log migrators

0016 and 0018 pair a schema change with a `RunPython` step (empty-string priority → NULL; copy `group` FK into `groups` M2M), and 0018 also defines `objectchange_migrators` to rewrite historical ObjectChange records. [code:netbox/tenancy/migrations/0016_charfield_null_choices.py:4-25] [code:netbox/tenancy/migrations/0018_contact_groups.py:5-10] [code:netbox/tenancy/migrations/0018_contact_groups.py:71-82]

0020 uses `SeparateDatabaseAndState` to drop the through model from Django's state while renaming the table, sequence, indexes and FK constraint in raw SQL so the data stays put. [code:netbox/tenancy/migrations/0020_remove_contactgroupmembership.py:11-70]
