# tenancy — subsystem map (NetBox @ ea4c205)

## What it is

`tenancy` is the Django app that owns two small object families: **Tenants** (Tenant, TenantGroup — "an organization served by the NetBox owner") and **Contacts** (Contact, ContactGroup, ContactRole, ContactAssignment). It is 41 non-test modules, 3,688 lines of code, four test modules, and no data files. [fg:subsystems:tenancy] [code:netbox/tenancy/models/tenants.py:36-40]

The app is registered in `INSTALLED_APPS`, mounted at `/tenancy/` and `/api/tenancy/`, and its GraphQL query type is merged into the root schema. [code:netbox/netbox/settings.py:435] [code:netbox/netbox/urls.py:31] [code:netbox/netbox/urls.py:50] [code:netbox/netbox/graphql/schema.py:13]

## Modules by role

- **Models** — `models/tenants.py` (TenantGroup, Tenant) and `models/contacts.py` (ContactGroup, ContactRole, Contact, ContactAssignment); `models/__init__.py` star-imports both. [fg:modules:tenancy.models.tenants] [fg:modules:tenancy.models.contacts] [code:netbox/tenancy/models/__init__.py:1-2]
- **Choices** — one ChoiceSet, `ContactPriorityChoices` (primary/secondary/tertiary/inactive). [fg:symbols:tenancy.choices:ContactPriorityChoices] [code:netbox/tenancy/choices.py:10-21]
- **Views** — `views.py`: 41 classes, all decorated with `register_model_view`, seven per model (list/detail/edit/delete/bulk_import/bulk_edit/bulk_delete) except ContactAssignment, which has no detail view. [fg:modules:tenancy.views] [code:netbox/tenancy/views.py:346-403]
- **URLs** — `urls.py` builds every route from `get_model_urls()`; it holds no hand-written paths. [fg:entrypoints:tenancy.urls] [code:netbox/tenancy/urls.py:7-27]
- **Forms** — a package: `forms.py` (reusable mixins TenancyForm, TenancyFilterForm, ContactModelFilterForm), `model_forms.py`, `bulk_edit.py`, `bulk_import.py`, `filtersets.py`; `__init__.py` star-imports all five. [fg:modules:tenancy.forms] [code:netbox/tenancy/forms/__init__.py:1-5] [fg:symbols:tenancy.forms.forms:TenancyForm]
- **Filtersets** — `filtersets.py`: six model filtersets plus two exportable mixins, `TenancyFilterSet` and `ContactModelFilterSet`, both plain `django_filters.FilterSet`. [fg:symbols:tenancy.filtersets:TenancyFilterSet] [fg:symbols:tenancy.filtersets:ContactModelFilterSet] [code:netbox/tenancy/filtersets.py:148-164]
- **Tables** — a package: `columns.py` (TenantColumn, TenantGroupColumn, TenancyColumnsMixin, ContactsColumnMixin), `template_code.py` (the two column templates), `tenants.py`, `contacts.py`. [fg:modules:tenancy.tables.columns] [fg:modules:tenancy.tables.template_code] [code:netbox/tenancy/tables/__init__.py:1-3]
- **REST API** — `api/views.py` (root view + six viewsets), `api/urls.py` (NetBoxRouter, six registrations), `api/serializers.py` re-exporting `serializers_/tenants.py`, `serializers_/contacts.py`, `serializers_/nested.py`. [fg:entrypoints:tenancy.api.views] [code:netbox/tenancy/api/urls.py:5-19] [code:netbox/tenancy/api/serializers.py:1-2]
- **GraphQL** — `graphql/types.py` (six strawberry types), `graphql/filters.py` (six filter types), `graphql/filter_mixins.py` (TenancyFilterMixin, ContactFilterMixin), `graphql/mixins.py` (ContactAssignmentsMixin), `graphql/enums.py`, `graphql/schema.py` (TenancyQuery). [fg:symbols:tenancy.graphql.schema:TenancyQuery] [code:netbox/tenancy/graphql/schema.py:9-27] [fg:symbols:tenancy.graphql.filter_mixins:TenancyFilterMixin]
- **Search** — `search.py`: five `@register_search` indexes (no index for ContactAssignment); it is imported for side effect from `apps.py`. [fg:modules:tenancy.search] [code:netbox/tenancy/search.py:5-18] [code:netbox/tenancy/search.py:44-65] [code:netbox/tenancy/apps.py:7-12]
- **Signals** — none; there is no `signals.py` in the module list. [fg:subsystems:tenancy]
- **Migrations** — 0001 (squashed, Tenant/TenantGroup), 0002 (squashed, adds Contact family), then 0012–0020 covering custom fields on ContactAssignment, GFK index, ordering, the content_type→object_type rename, nullable priority, natural-sort collation, Contact.group→groups M2M, comments on groups, and dropping the explicit through model. [fg:modules:tenancy.migrations.0001_squashed_0012] [fg:modules:tenancy.migrations.0002_squashed_0011] [code:netbox/tenancy/migrations/0018_contact_groups.py:19-68] [code:netbox/tenancy/migrations/0020_remove_contactgroupmembership.py:11-34]
- **Tests** — `test_api.py`, `test_views.py`, `test_filtersets.py`, one class per model, built on `utilities.testing` base cases; there are no model or form tests. [fg:modules:tenancy.tests.test_api] [fg:modules:tenancy.tests.test_views] [fg:modules:tenancy.tests.test_filtersets]

## Model shape

Tenant is `ContactsMixin + PrimaryModel` with an optional FK to TenantGroup (SET_NULL) and four UniqueConstraints: name and slug unique per group, and unique globally when group is null. [fg:symbols:tenancy.models.tenants:Tenant] [fg:model_refs:tenancy.models.tenants:50] [code:netbox/tenancy/models/tenants.py:62-85]

TenantGroup and ContactGroup are both `NestedGroupModel` (MPTT), but they differ: TenantGroup re-declares `name` and `slug` as globally `unique=True`, while ContactGroup keeps the base fields and adds a `(parent, name)` UniqueConstraint. [code:netbox/tenancy/models/tenants.py:14-28] [code:netbox/tenancy/models/contacts.py:20-31] [code:netbox/netbox/models/__init__.py:128-158]

ContactAssignment is not a NetBoxModel: it is `CustomFieldsMixin, ExportTemplatesMixin, TagsMixin, ChangeLoggedModel` with a GenericForeignKey (`object_type`/`object_id`), PROTECT FKs to Contact and ContactRole, a nullable `priority`, and a `(object_type, object_id, contact, role)` UniqueConstraint. [fg:symbols:tenancy.models.contacts:ContactAssignment] [fg:model_refs:tenancy.models.contacts:99] [code:netbox/tenancy/models/contacts.py:98-138]

Contact carries a `groups` M2M to ContactGroup (`related_query_name='contact'`), and name fields on Contact, Tenant and TenantGroup use the `natural_sort` collation. [fg:model_refs:tenancy.models.contacts:50] [code:netbox/tenancy/models/contacts.py:50-60] [code:netbox/tenancy/migrations/0017_natural_ordering.py:10-25]

## Entry points

- `tenancy.urls` — UI routes, mounted at `/tenancy/`. [fg:entrypoints:tenancy.urls] [code:netbox/netbox/urls.py:31]
- `tenancy.api.urls` / `tenancy.api.views` — REST routes at `/api/tenancy/` (`tenant-groups`, `tenants`, `contact-groups`, `contact-roles`, `contacts`, `contact-assignments`). [fg:entrypoints:tenancy.api.urls] [fg:entrypoints:tenancy.api.views] [code:netbox/tenancy/api/urls.py:8-16]
- `TenancyQuery` — GraphQL, merged into the root schema. [code:netbox/tenancy/graphql/schema.py:9-27] [fg:imports:netbox.graphql.schema->tenancy.graphql.schema]
- `TenancyConfig.ready()` — calls `register_models()` on every model and imports `search`. [code:netbox/tenancy/apps.py:7-12] [fg:imports:tenancy.apps->netbox.models.features]
- Navigation: Tenants, Tenant Groups, Contacts, Contact Groups, Contact Roles are menu items in the core menu. [code:netbox/netbox/navigation/menu.py:26-35]

## What it depends on

Outbound edges: 56 internal, 27 to `netbox`, 22 to `utilities`, 6 to `core`, and 2 each to circuits/extras/ipam/virtualization/vpn/wireless. [fg:subsystems:tenancy] [fg:imports:tenancy.filtersets->netbox.filtersets] [fg:imports:tenancy.forms.model_forms->utilities.forms.fields]

The six peer-app edges come only from GraphQL: `graphql/types.py` and `graphql/filters.py` declare reverse relations from Tenant to every model that carries a `tenant` FK, using `strawberry.lazy` string references under `TYPE_CHECKING`. [fg:imports:tenancy.graphql.types->dcim.graphql.types] [fg:imports:tenancy.graphql.filters->ipam.graphql.filters] [code:netbox/tenancy/graphql/types.py:12-38] [code:netbox/tenancy/graphql/filters.py:18-47]

`core.models.ObjectType.with_feature('contacts')` is used for validation in `ContactAssignment.clean()` and to scope the object-type choices in `ContactAssignmentFilterForm`. [fg:imports:tenancy.models.contacts->core.models] [fg:imports:tenancy.forms.filtersets->core.models] [code:netbox/tenancy/models/contacts.py:150-157] [code:netbox/tenancy/forms/filtersets.py:89-93]

The REST serializer for Tenant hard-codes ten `RelatedObjectCountField`s (circuits, devices, racks, sites, ip_addresses, prefixes, vlans, vrfs, virtual_machines, clusters) — a string-level dependency on reverse accessors in five other apps. [code:netbox/tenancy/api/serializers_/tenants.py:30-40]

Tests depend on `dcim.models.Site` (and Manufacturer) to have something to assign contacts to. [fg:imports:tenancy.tests.test_api->dcim.models] [fg:imports:tenancy.tests.test_filtersets->dcim.models] [code:netbox/tenancy/tests/test_views.py:253-259]

## What depends on it

Inbound: dcim 23, ipam 18, wireless 14, virtualization 13, circuits 12, extras 11, vpn 11, netbox 6. [fg:subsystems:tenancy]

By import kind, every consuming app follows the same five-file pattern: `tenancy.models` (bulk_edit/bulk_import/tests), `tenancy.forms` (TenancyForm / TenancyFilterForm / ContactModelFilterForm in model_forms and filtersets), `tenancy.filtersets` (TenancyFilterSet, ContactModelFilterSet), `tenancy.tables` (TenancyColumnsMixin, ContactsColumnMixin, TenantColumn), `tenancy.api.serializers_.tenants` (TenantSerializer nested in the consumer's serializer), and `tenancy.graphql.filter_mixins` / `tenancy.graphql.types`. [fg:imports:dcim.forms.model_forms->tenancy.forms] [fg:imports:dcim.filtersets->tenancy.filtersets] [fg:imports:dcim.tables.sites->tenancy.tables] [fg:imports:dcim.api.serializers_.devices->tenancy.api.serializers_.tenants] [fg:imports:dcim.graphql.filters->tenancy.graphql.filter_mixins] [code:netbox/dcim/filtersets.py:146]

By string reference, 27 models in six apps (circuits 3, dcim 8, ipam 10, virtualization 2, vpn 2, wireless 2) hold a `ForeignKey -> tenancy.Tenant` named `tenant`, and `extras.ConfigContext` has M2Ms to both Tenant and TenantGroup. [fg:model_refs:dcim.models.devices:462] [fg:model_refs:ipam.models.ip:219] [fg:model_refs:vpn.models.tunnels:62] [fg:model_refs:extras.models.configs:100] [fg:model_refs:extras.models.configs:105]

The `netbox` core app is a two-way dependency: `netbox.models.features.ContactsMixin` is a `GenericRelation -> tenancy.ContactAssignment` and lazily imports `ContactAssignment` inside `get_contacts()`; `register_models()` auto-registers an `ObjectContactsView` for every ContactsMixin model; and `netbox.views.generic.feature_views.ObjectContactsView` imports the tenancy model, table, filterset and filter form. [fg:model_refs:netbox.models.features:366] [fg:imports:netbox.models.features->tenancy.models] [code:netbox/netbox/models/features.py:362-395] [code:netbox/netbox/models/features.py:673-676] [code:netbox/netbox/views/generic/feature_views.py:15-18] [code:netbox/netbox/views/generic/feature_views.py:255-274]

`extras.graphql.mixins.ContactsMixin` lazily references `tenancy.graphql.types.ContactAssignmentType`, and `tenancy.graphql.types` in turn imports that mixin — a cycle resolved only through `strawberry.lazy`. [fg:imports:extras.graphql.mixins->tenancy.graphql.types] [fg:imports:tenancy.graphql.types->extras.graphql.mixins] [code:netbox/extras/graphql/mixins.py:59-61]

Column templates also reach into ipam by attribute name: `TENANT_COLUMN` falls back to `record.vrf.tenant` (marked with `*`) when the row has no tenant of its own, which only ipam tables using `TenancyColumnsMixin` can satisfy. [code:netbox/tenancy/tables/template_code.py:1-19] [code:netbox/ipam/tables/ip.py:157]

## Where change concentrates

`views.py` dominates: 144 commits, 16 authors, 2016–2025. Next are `api/serializers.py` (58, but now a two-line re-export), `api/views.py` (42), `filtersets.py` (38), `tests/test_api.py` (34), `models/contacts.py` (33, all since 2021-10) and `urls.py` (31). [fg:churn:tenancy.views] [fg:churn:tenancy.api.serializers] [fg:churn:tenancy.api.views] [fg:churn:tenancy.filtersets] [fg:churn:tenancy.models.contacts] [fg:churn:tenancy.urls]

The Contact family is where recent change lives: `models/contacts.py` last changed 2025-05-09, `api/serializers_/contacts.py` 2025-04-11, `tables/contacts.py` 2025-04-10, and migrations 0018–0020 (2025-03 to 2025-06) reworked Contact↔ContactGroup from FK to M2M. [fg:churn:tenancy.models.contacts] [fg:churn:tenancy.api.serializers_.contacts] [fg:churn:tenancy.tables.contacts] [code:netbox/tenancy/migrations/0018_contact_groups.py:48-67]

The Tenant side is comparatively stable: `models/tenants.py` has 14 commits by 3 authors, last touched 2024-11-15. [fg:churn:tenancy.models.tenants]

## Things to know before editing

- ContactAssignment has no detail page: `get_absolute_url()` redirects to the owning Contact, the list view enables only export/bulk actions, and the table's actions column offers only edit/delete. [code:netbox/tenancy/models/contacts.py:147-148] [code:netbox/tenancy/views.py:352-357] [code:netbox/tenancy/tables/contacts.py:143-145]
- `ContactAssignmentTable.contact_group` still uses accessor `contact__group`, but Contact has had only `groups` (M2M) since migration 0018. [code:netbox/tenancy/tables/contacts.py:109-113] [code:netbox/tenancy/migrations/0018_contact_groups.py:64-67]
- The ContactAssignment REST serializer declares `role` as `required=False, allow_null=True` and defaults `priority` to `''`, whereas the model's `role` FK is non-null and migration 0016 rewrote empty priorities to NULL. [code:netbox/tenancy/api/serializers_/contacts.py:69-70] [code:netbox/tenancy/models/contacts.py:113-124] [code:netbox/tenancy/migrations/0016_charfield_null_choices.py:4-11]
- The bulk-import form accepts any ContentType for `object_type`; the "supports contacts" check happens only in `ContactAssignment.clean()`. [code:netbox/tenancy/forms/bulk_import.py:93-96] [code:netbox/tenancy/models/contacts.py:150-157]
