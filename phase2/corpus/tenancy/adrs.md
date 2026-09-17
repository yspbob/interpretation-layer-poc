# tenancy — retro-ADRs (NetBox @ ea4c205)

Decisions the code embodies that no document records; each is stated as the code has it, not as a recommendation, and the subsystem summary is the frame for all of them. [fg:subsystems:tenancy]

## ADR-T1. Contacts attach to any object through one generic join model, gated by a registry feature

**Context.** Contacts were added to the tenancy app in 2021 (migration 0002 creates ContactRole, ContactGroup, Contact and ContactAssignment together) and had to be attachable to sites, devices, circuits and more without a schema change per model. [code:netbox/tenancy/migrations/0002_squashed_0011.py:34-35] [code:netbox/tenancy/migrations/0002_squashed_0011.py:146-157] [fg:churn:tenancy.models.contacts]

**Decision.** `ContactAssignment` holds a GenericForeignKey (`object_type`, `object_id`) plus FKs to Contact and ContactRole and an optional priority; a model opts in by mixing in `ContactsMixin`, which is a `GenericRelation` back to the assignment; eligibility is checked at runtime against `ObjectType.objects.with_feature('contacts')`. [code:netbox/tenancy/models/contacts.py:98-124] [fg:model_refs:netbox.models.features:366] [code:netbox/tenancy/models/contacts.py:150-157]

**Consequences.** The "contacts" tab, its view and its permission are registered automatically for every ContactsMixin model, so tenancy has no per-app code; in exchange the assignment table needs a composite `(object_type, object_id)` index, the change log must be told the related object explicitly, and uniqueness is `(object_type, object_id, contact, role)`. Contact inheritance up an MPTT tree comes for free in `get_contacts(inherited=True)`. [code:netbox/netbox/models/features.py:673-676] [code:netbox/tenancy/models/contacts.py:128-138] [code:netbox/tenancy/models/contacts.py:159-162] [code:netbox/netbox/models/features.py:375-395]

**Evidence.** Twenty-two concrete models in seven apps (including Tenant itself) carry `ContactsMixin`, e.g. Region, Site, Rack, Prefix, Circuit, VirtualMachine, Tunnel; the object-type filter form is scoped by the same feature query. [code:netbox/dcim/models/sites.py:24] [code:netbox/dcim/models/sites.py:136] [code:netbox/ipam/models/ip.py:201] [code:netbox/circuits/models/circuits.py:38] [code:netbox/tenancy/models/tenants.py:36] [code:netbox/tenancy/forms/filtersets.py:89-93]

## ADR-T2. Tenant is referenced by a plain FK on each model; tenancy support in the other layers is delivered as mixins

**Context.** Twenty-seven models in six apps need an optional tenant, and every one of them needs the same form fields, filter fields, table columns and GraphQL filter arguments. [fg:model_refs:dcim.models.sites:173] [fg:model_refs:ipam.models.vrfs:32] [fg:model_refs:circuits.models.circuits:72]

**Decision.** No abstract "TenantModel" exists; each consuming model declares `tenant = ForeignKey('tenancy.Tenant')` itself, and the UI/API layers reuse exported mixins: `TenancyForm`, `TenancyFilterForm`, `TenancyFilterSet`, `TenancyColumnsMixin`, `TenancyFilterMixin`. [code:netbox/tenancy/forms/forms.py:14-50] [code:netbox/tenancy/filtersets.py:231-257] [code:netbox/tenancy/tables/columns.py:44-50] [code:netbox/tenancy/graphql/filter_mixins.py:27-38]

**Consequences.** Adding a tenant-able model means touching five layers in the consuming app, but the tenancy app never changes; the mixins are plain `FilterSet`/`Form`/`Table` classes and depend on the consumer's MRO for `Meta`. The inbound import graph is therefore wide (108 edges) but shallow — almost all edges land on `tenancy.models`, `tenancy.forms`, `tenancy.filtersets`, `tenancy.tables`. [fg:subsystems:tenancy] [fg:symbols:tenancy.filtersets:TenancyFilterSet] [fg:imports:dcim.forms.model_forms->tenancy.forms] [fg:imports:vpn.filtersets->tenancy.filtersets]

**Evidence.** `SiteForm(TenancyForm, NetBoxModelForm)`, `SiteFilterSet(NetBoxModelFilterSet, TenancyFilterSet, ContactModelFilterSet)`, `PrefixTable(TenancyColumnsMixin, NetBoxTable)`. [code:netbox/dcim/forms/model_forms.py:117] [code:netbox/dcim/filtersets.py:146] [code:netbox/ipam/tables/ip.py:157]

## ADR-T3. Tenancy owns the reverse-relation catalogue for Tenant in GraphQL and REST

**Context.** GraphQL consumers want to walk from a tenant to its devices, prefixes, circuits etc., and the REST Tenant payload exposes related-object counts. [code:netbox/tenancy/graphql/types.py:60-85] [code:netbox/tenancy/api/serializers_/tenants.py:30-40]

**Decision.** `TenantType` and `TenantFilter` enumerate every reverse relation by hand (24 list fields, 27 filter fields), importing peer-app types only under `TYPE_CHECKING` and binding them with `strawberry.lazy`; `TenantSerializer` hard-codes ten `RelatedObjectCountField`s. [code:netbox/tenancy/graphql/types.py:12-38] [code:netbox/tenancy/graphql/filters.py:70-107] [code:netbox/tenancy/graphql/filters.py:108-135] [code:netbox/tenancy/api/serializers_/tenants.py:30-40]

**Consequences.** This is the only place tenancy depends on circuits, dcim, ipam, virtualization, vpn and wireless (two edges each), and it makes tenancy a mandatory edit whenever a peer app adds or renames a `tenant` relation. The REST count list is already narrower than the FK set (no counts for cables, tunnels, L2VPNs, ASNs, wireless objects). [fg:imports:tenancy.graphql.types->circuits.graphql.types] [fg:imports:tenancy.graphql.filters->wireless.graphql.filters] [code:netbox/tenancy/api/serializers_/tenants.py:31-40] [fg:model_refs:dcim.models.cables:54]

**Evidence.** The mirror-image lazy reference exists in extras: `ContactsMixin.contacts` points back to `tenancy.graphql.types.ContactAssignmentType`. [code:netbox/extras/graphql/mixins.py:59-61] [fg:imports:extras.graphql.mixins->tenancy.graphql.types]

## ADR-T4. Tenant names and slugs are unique per group, and globally unique only when ungrouped

**Context.** TenantGroup keeps `name` and `slug` globally unique, but a Tenant belongs to an optional group and the same tenant name must be allowed under different groups. [code:netbox/tenancy/models/tenants.py:18-28]

**Decision.** Four `UniqueConstraint`s: `(group, name)` and `(group, slug)` unconditionally, plus `(name)` and `(slug)` with `condition=Q(group__isnull=True)`. [code:netbox/tenancy/models/tenants.py:64-85]

**Consequences.** Two ungrouped tenants cannot share a name, but a grouped and an ungrouped tenant can; `slug` lookups in filters (`tenant=<slug>`) therefore may match several rows and are declared as multiple-choice filters. [code:netbox/tenancy/filtersets.py:252-257] [code:netbox/tenancy/models/tenants.py:70-74]

**Evidence.** ContactGroup took a different route — `(parent, name)` only, slug not constrained — showing the choice was made per model, not in `NestedGroupModel`. [code:netbox/tenancy/models/contacts.py:24-31] [code:netbox/netbox/models/__init__.py:128-158]

## ADR-T5. Contact↔ContactGroup became many-to-many, keeping Django's default M2M table name

**Context.** Contact originally had a single `group` FK with a `(group, name)` uniqueness rule. [code:netbox/tenancy/migrations/0018_contact_groups.py:30-33] [code:netbox/tenancy/migrations/0018_contact_groups.py:64-67]

**Decision.** In two steps: 0018 introduced an explicit `ContactGroupMembership` through model, copied every FK into it and dropped `group`; 0020 then removed the through model from Django state while renaming the table, sequence, indexes and constraint in SQL to what an implicit M2M would have generated. [code:netbox/tenancy/migrations/0018_contact_groups.py:19-68] [code:netbox/tenancy/migrations/0020_remove_contactgroupmembership.py:11-70]

**Consequences.** The model is a plain `ManyToManyField(related_query_name='contact')`; bulk edit needs `add_groups`/`remove_groups` plus custom `post_save_operations`; the `(group, name)` uniqueness on Contact is gone; historical ObjectChange rows are rewritten by an `objectchange_migrators` hook. One straggler remains — `ContactAssignmentTable.contact_group` still reads `contact__group`. [code:netbox/tenancy/models/contacts.py:50-55] [code:netbox/tenancy/views.py:323-330] [code:netbox/tenancy/migrations/0018_contact_groups.py:71-82] [code:netbox/tenancy/tables/contacts.py:109-113]

**Evidence.** Group filters on Contact and ContactAssignment now traverse `groups` / `contact__groups` with tree semantics. [code:netbox/tenancy/filtersets.py:68-80] [code:netbox/tenancy/filtersets.py:111-123]

## ADR-T6. ContactAssignment is a change-logged record, not a first-class page

**Context.** An assignment is meaningful only in the context of its contact and its target object. [code:netbox/tenancy/models/contacts.py:142-145]

**Decision.** ContactAssignment inherits `ChangeLoggedModel` plus `CustomFieldsMixin`, `ExportTemplatesMixin`, `TagsMixin` (not `NetBoxModel`), has no detail view, sends `get_absolute_url()` to the contact, and is created from the target object's Contacts tab via `?object_type=&object_id=`. [fg:symbols:tenancy.models.contacts:ContactAssignment] [code:netbox/tenancy/models/contacts.py:147-148] [code:netbox/tenancy/views.py:360-377] [code:netbox/netbox/views/generic/feature_views.py:255-274]

**Consequences.** No search index, no journaling/bookmarks/notifications, list actions limited to export and bulk operations, table actions limited to edit/delete; custom fields were bolted on later (0012). Change-log entries point at the target object via `related_object`. [code:netbox/tenancy/search.py:5-18] [code:netbox/tenancy/search.py:44-65] [code:netbox/tenancy/views.py:352-357] [code:netbox/tenancy/migrations/0012_contactassignment_custom_fields.py:12-18] [code:netbox/tenancy/models/contacts.py:159-162]

**Evidence.** The view test composes only Create/Edit/Delete/List/BulkEdit/BulkDelete cases. [code:netbox/tenancy/tests/test_views.py:240-248]

## ADR-T7. "No choice" is NULL, not the empty string, for choice CharFields

**Context.** `priority` on ContactAssignment was a blank CharField storing `''` for "unset". [code:netbox/tenancy/migrations/0016_charfield_null_choices.py:19-24]

**Decision.** Migration 0016 made the column nullable and rewrote existing `''` to NULL; the model now declares `blank=True, null=True`. [code:netbox/tenancy/migrations/0016_charfield_null_choices.py:4-25] [code:netbox/tenancy/models/contacts.py:118-124]

**Consequences.** `__str__` and ordering treat unset priority as falsy/NULL; the REST serializer, however, still defaults `priority` to `''` with `allow_blank=True`, so API-created rows may carry the empty string the migration removed. [code:netbox/tenancy/models/contacts.py:142-145] [code:netbox/tenancy/api/serializers_/contacts.py:70]

**Evidence.** Bulk-edit lists `priority` as the only nullable field on the assignment form. [code:netbox/tenancy/forms/bulk_edit.py:158-168]
