# vpn — patterns and conventions (NetBox @ ea4c205)

## 1. One-model-seven-views, registered by decorator, no hand-written URLs

Every model gets the same seven `netbox.views.generic` subclasses (list, detail, edit, delete, bulk import/edit/delete), each decorated with `register_model_view`; the edit view is registered as both `add` (detail=False) and `edit`. Compare TunnelGroup and IPSecProfile [code:netbox/vpn/views.py:13-67] [code:netbox/vpn/views.py:388-431]. `urls.py` never names a view; it includes `get_model_urls(...)` twice per model [code:netbox/vpn/urls.py:9-37]. Adding a view means adding a decorated class [fg:entrypoints:vpn.urls].

**Exception**: TunnelEditView overrides `dispatch` to substitute TunnelCreateForm when no `pk` is in kwargs, so the same registered view serves two forms [code:netbox/vpn/views.py:91-101]. TunnelGroupView is the only detail view that mixes in GetRelatedModelsMixin; L2VPNView is the only one that builds extra tables (import/export RouteTargetTable) in `get_extra_context` [code:netbox/vpn/views.py:23-30] [code:netbox/vpn/views.py:446-465].

## 2. List/bulk querysets carry a count annotation that the table reads through an accessor

Where a table shows a related count, the list, bulk-edit and bulk-delete views annotate with `count_related` and the table declares a LinkedCountColumn. TunnelGroup annotates `tunnel_count` in three views [code:netbox/vpn/views.py:15-17] [code:netbox/vpn/views.py:53-55] [code:netbox/vpn/views.py:63-65], read by TunnelGroupTable.tunnel_count [code:netbox/vpn/tables/tunnels.py:21-25]. Tunnel annotates `count_terminations` [code:netbox/vpn/views.py:76-78] [code:netbox/vpn/views.py:117-119], read via `Accessor('count_terminations')` on TunnelTable.terminations_count [code:netbox/vpn/tables/tunnels.py:54-59].

**Exception**: TunnelTable.Meta.fields lists `termination_count` while the declared column is `terminations_count`, so Meta names a column that does not exist [code:netbox/vpn/tables/tunnels.py:54] [code:netbox/vpn/tables/tunnels.py:69-72].

## 3. Dual filters per relation: `<name>_id` by PK and `<name>` by natural key

Every filterable FK/M2M is declared twice: a ModelMultipleChoiceFilter on the PK and one on the natural key (`slug` or `name`). TunnelFilterSet.group/group_id use slug [code:netbox/vpn/filtersets.py:39-48]; IPSecProfileFilterSet.ike_policy/ike_policy_id use name [code:netbox/vpn/filtersets.py:261-270]; L2VPNTerminationFilterSet.l2vpn/l2vpn_id use slug [code:netbox/vpn/filtersets.py:343-352]. Reverse M2M filters follow the same shape (`ike_policy_id` on IKEProposal, `ipsec_policy_id` on IPSecProposal) [code:netbox/vpn/filtersets.py:127-137] [code:netbox/vpn/filtersets.py:197-207].

**Exceptions**: IKEPolicyFilterSet.ike_proposal/ike_proposal_id and IPSecPolicyFilterSet.ipsec_proposal/ipsec_proposal_id carry no `label` [code:netbox/vpn/filtersets.py:172-180] [code:netbox/vpn/filtersets.py:233-241]. TunnelTerminationFilterSet has `outside_ip_id` but no `outside_ip` natural-key twin [code:netbox/vpn/filtersets.py:115-119].

## 4. `search()` is copy-pasted per FilterSet over name/description/comments

Six FilterSets define an identical `search` body over `name | description | comments`: Tunnel, IKEProposal, IKEPolicy, IPSecProposal, IPSecPolicy, IPSecProfile [code:netbox/vpn/filtersets.py:67-74] [code:netbox/vpn/filtersets.py:155-162] [code:netbox/vpn/filtersets.py:286-293].

**Exceptions**: L2VPNFilterSet.search omits comments and adds an integer match on `identifier` [code:netbox/vpn/filtersets.py:331-339]; L2VPNTerminationFilterSet searches only `l2vpn__name` [code:netbox/vpn/filtersets.py:438-442]; TunnelGroup and TunnelTermination define none [code:netbox/vpn/filtersets.py:28-32] [code:netbox/vpn/filtersets.py:77-123].

## 5. Generic terminations: ContentType FK + GenericForeignKey, uniqueness enforced twice

Both termination models pair a PROTECTed `ContentType` FK (`related_name='+'`) with a PositiveBigIntegerField and GenericForeignKey, plus a UniqueConstraint on (type, id) so an object terminates at most one tunnel/L2VPN [code:netbox/vpn/models/tunnels.py:114-126] [code:netbox/vpn/models/tunnels.py:141-147] [code:netbox/vpn/models/l2vpn.py:93-102] [code:netbox/vpn/models/l2vpn.py:111-116]. Each model re-checks the rule in `clean()` for a field-level ValidationError [code:netbox/vpn/models/tunnels.py:160-170] [code:netbox/vpn/models/l2vpn.py:125-136]. Migration 0009 dropped the separate `(type, id)` indexes as redundant with the unique constraints [code:netbox/vpn/migrations/0009_remove_redundant_indexes.py:13-20].

The reverse side is declared by the target apps as `GenericRelation` with `related_query_name` `interface` / `vminterface` / `vlan`, and vpn filtersets query through those names [fg:model_refs:dcim.models.device_components:781] [fg:model_refs:virtualization.models.virtualmachines:350] [fg:model_refs:ipam.models.vlans:246] [code:netbox/vpn/filtersets.py:373-431].

**Difference between the two**: TunnelTermination.termination_id is nullable, L2VPNTermination.assigned_object_id is not [code:netbox/vpn/models/tunnels.py:119-122] [code:netbox/vpn/models/l2vpn.py:98]. TunnelTermination.clean relies on a `tunnel_termination` attribute on the target object, whereas L2VPNTermination.clean runs an explicit queryset [code:netbox/vpn/models/tunnels.py:164] [code:netbox/vpn/models/l2vpn.py:130-131].

## 6. Forms resolve the GFK via a type switch plus parent/child dynamic fields, then set it in `clean()`

Model forms never expose the ContentType field. TunnelTerminationForm shows a `type` ChoiceField (HTMXSelect), a `parent` (Device) and a `termination` (Interface) DynamicModelChoiceField, swaps the querysets to VirtualMachine/VMInterface in `__init__` when type is VM, and assigns `self.instance.termination` in `clean()` [code:netbox/vpn/forms/model_forms.py:229-253] [code:netbox/vpn/forms/model_forms.py:273-293]. TunnelCreateForm repeats this twice for `termination1_*` and `termination2_*` [code:netbox/vpn/forms/model_forms.py:76-108] [code:netbox/vpn/forms/model_forms.py:160-180]. L2VPNTerminationForm instead exposes three optional fields in TabbedGroups (vlan/interface/vminterface), requires exactly one, and assigns `assigned_object` in `clean()` [code:netbox/vpn/forms/model_forms.py:451-461] [code:netbox/vpn/forms/model_forms.py:482-494].

Bulk-import forms do likewise with CSV columns: `device` / `virtual_machine` narrow the `termination` (or `interface`) queryset in `__init__` from an initial `Interface.objects.none()`, and the GFK is set in `save()` (Tunnel) or `clean()` (L2VPN) [code:netbox/vpn/forms/bulk_import.py:99-105] [code:netbox/vpn/forms/bulk_import.py:119-140] [code:netbox/vpn/forms/bulk_import.py:301-307] [code:netbox/vpn/forms/bulk_import.py:320-347].

**Exception**: TunnelCreateForm.clean's `if any(...)` sits outside the `for term in (...)` loop, so only the last iteration's (`termination2`) parameters are validated [code:netbox/vpn/forms/model_forms.py:182-199]. View tests exclude `termination` from form validation with a TODO about the form-field/GFK conflict [code:netbox/vpn/tests/test_views.py:119-122].

## 7. Serializers: ChoiceField per choice, nested serializer per FK, SerializedPKRelatedField per M2M, method field for the GFK

Choice fields are wrapped in `ChoiceField(choices=...)` [code:netbox/vpn/api/serializers_/crypto.py:16-28] [code:netbox/vpn/api/serializers_/tunnels.py:40-51]. FKs are the target serializer with `nested=True` [code:netbox/vpn/api/serializers_/crypto.py:111-116] [code:netbox/vpn/api/serializers_/tunnels.py:43-61]. M2Ms use SerializedPKRelatedField [code:netbox/vpn/api/serializers_/crypto.py:48-54] [code:netbox/vpn/api/serializers_/l2vpn.py:22-35]. The GFK target is a read-only SerializerMethodField that dispatches through `get_serializer_for_model` with `nested=True` [code:netbox/vpn/api/serializers_/tunnels.py:103-109] [code:netbox/vpn/api/serializers_/l2vpn.py:65-69]. Every Meta declares `brief_fields` [code:netbox/vpn/api/serializers_/tunnels.py:36] [code:netbox/vpn/api/serializers_/l2vpn.py:45].

**Exception**: `get_termination` guards against a null GFK; `get_assigned_object` does not, matching the non-null `assigned_object_id` [code:netbox/vpn/api/serializers_/tunnels.py:105-106] [code:netbox/vpn/api/serializers_/l2vpn.py:66-69].

## 8. Star-imports through `__all__`-guarded package modules

Every sub-package (`models`, `forms`, `tables`, `api.serializers`) is assembled by `from .x import *` [code:netbox/vpn/api/serializers.py:1-3] [fg:imports:vpn.models->vpn.models.tunnels] [fg:imports:vpn.forms->vpn.forms.model_forms] [fg:imports:vpn.tables->vpn.tables.crypto], and every leaf module declares a sorted `__all__` [code:netbox/vpn/models/crypto.py:8-14] [code:netbox/vpn/filtersets.py:14-25] [code:netbox/vpn/views.py:5-6]. Consumers star-import `vpn.models` and `vpn.choices` [code:netbox/vpn/filtersets.py:11-12] [code:netbox/vpn/forms/bulk_edit.py:9-10].

## 9. Nullable choice CharFields use `null=True`, not empty string

Optional choice fields (IKEPolicy.mode, IKEProposal/IPSecProposal algorithms) are `blank=True, null=True` with no `max_length` [code:netbox/vpn/models/crypto.py:36-41] [code:netbox/vpn/models/crypto.py:79-84] [code:netbox/vpn/models/crypto.py:133-144]; migration 0006 converted stored empty strings to NULL [code:netbox/vpn/migrations/0006_charfield_null_choices.py:13-16] [fg:model_refs:vpn.migrations.0006_charfield_null_choices:8]. The filter form for L2VPN type passes `null_value=None` for the same reason [code:netbox/vpn/filtersets.py:297-300].

**Exception**: IKEPolicy.preshared_key is a TextField with `blank=True` and no `null` [code:netbox/vpn/models/crypto.py:90-93].

## 10. Every `name` is unique with `natural_sort` collation; slugs only on TunnelGroup and L2VPN

All seven named models declare `name` as `unique=True, db_collation="natural_sort"` [code:netbox/vpn/models/tunnels.py:31-36] [code:netbox/vpn/models/crypto.py:22-27] [code:netbox/vpn/models/l2vpn.py:19-24], applied in migration 0007 [code:netbox/vpn/migrations/0007_natural_ordering.py:11-45]. Only TunnelGroup and L2VPN carry a `slug` [code:netbox/vpn/models/l2vpn.py:25-29] [code:netbox/vpn/forms/model_forms.py:33] [code:netbox/vpn/forms/model_forms.py:398].

Models with dependencies also declare `prerequisite_models` (IKEPolicy, IPSecProfile, both terminations) [code:netbox/vpn/models/crypto.py:98-100] [code:netbox/vpn/models/tunnels.py:135-137] [code:netbox/vpn/models/l2vpn.py:105-107].

**Exception**: Tunnel is also unique on `(group, name)` plus a conditional constraint on name when group is null, which the plain `unique=True` already makes redundant [code:netbox/vpn/models/tunnels.py:81-91].

## 11. GraphQL: `fields='__all__'` types, lazy relation annotations, enums from ChoiceSets

Nine of ten types use `fields='__all__'` and annotate every relation with `strawberry.lazy` module paths [code:netbox/vpn/graphql/types.py:32-40] [code:netbox/vpn/graphql/types.py:55-66]. Enums are built with `Choices.as_enum(prefix=...)` [code:netbox/vpn/graphql/enums.py:20-31]. Filters use `strawberry_django.filter_type(..., lookups=True)` on the shared mixins [code:netbox/vpn/graphql/filters.py:59-61] [code:netbox/vpn/graphql/filters.py:158-160].

**Exceptions**: L2VPNTerminationType uses `exclude=[...]` and a resolver returning a `strawberry.union` of the three target types [code:netbox/vpn/graphql/types.py:142-157]. The five crypto types and TunnelGroupType subclass OrganizationalObjectType even though the crypto models are PrimaryModels [code:netbox/vpn/graphql/types.py:75] [code:netbox/vpn/graphql/types.py:121] [fg:symbols:vpn.models.crypto:IKEProposal]. There is no L2VPNStatusEnum and L2VPNFilter has no `status` field, although the REST filterset and model have one [code:netbox/vpn/graphql/enums.py:5-18] [code:netbox/vpn/graphql/filters.py:158-174] [code:netbox/vpn/filtersets.py:301-303].

## 12. Filter forms mirror filtersets with `FieldSet` groups and `TagFilterField(model)`

Each filter form sets `model`, a `fieldsets` tuple starting with `('q', 'filter_id', 'tag')`, and ends with `tag = TagFilterField(model)` [code:netbox/vpn/forms/filtersets.py:33-39] [code:netbox/vpn/forms/filtersets.py:190-211].

**Exceptions**: IPSecPolicyFilterForm.proposal_id queries `IKEProposal` rather than IPSecProposal, its `pfs_group` is labelled "Mode", and neither IKEPolicyFilterForm.proposal_id nor IPSecPolicyFilterForm.proposal_id matches the filterset names `ike_proposal_id` / `ipsec_proposal_id` [code:netbox/vpn/forms/filtersets.py:144-148] [code:netbox/vpn/forms/filtersets.py:177-186] [code:netbox/vpn/filtersets.py:172-175] [code:netbox/vpn/filtersets.py:233-236]. L2VPNTerminationFilterForm omits `q` and `tag` entirely [code:netbox/vpn/forms/filtersets.py:247-253].

## 13. Bulk-edit forms: blank-choice ChoiceFields, `nullable_fields`, `model` attribute

Bulk-edit forms wrap ChoiceSets with `add_blank_choice`, set `required=False` on everything, and list `nullable_fields` [code:netbox/vpn/forms/bulk_edit.py:37-82] [code:netbox/vpn/forms/bulk_edit.py:95-136].

**Exceptions**: L2VPNTerminationBulkEditForm declares `model = L2VPN`, not L2VPNTermination, and has no fields [code:netbox/vpn/forms/bulk_edit.py:291-292]. TunnelBulkEditForm.ipsec_profile is a DynamicModelMultipleChoiceField although the model field is a single FK [code:netbox/vpn/forms/bulk_edit.py:53-57] [code:netbox/vpn/models/tunnels.py:55-61]. L2VPNBulkEditForm.status has no blank choice and is required [code:netbox/vpn/forms/bulk_edit.py:263-266].

## 14. Tests: one case per model per layer, built on utilities.testing

test_api, test_filtersets and test_views each define one class per model on the shared utilities.testing bases [fg:symbols:vpn.tests.test_api:TunnelTest] [fg:symbols:vpn.tests.test_filtersets:TunnelTestCase] [fg:symbols:vpn.tests.test_views:TunnelTestCase] [fg:imports:vpn.tests.test_api->utilities.testing]. Tests build dcim/ipam/virtualization fixtures directly [fg:imports:vpn.tests.test_views->dcim.models] [fg:imports:vpn.tests.test_filtersets->virtualization.models].

**Exceptions**: L2VPNTerminationTestCase composes eight individual ViewTestCases mixins instead of PrimaryObjectViewTestCase, dropping the bulk-edit case [code:netbox/vpn/tests/test_views.py:621-632]. test_models exists only for L2VPNTermination, and its "vlan" duplicate test actually fetches an Interface [code:netbox/vpn/tests/test_models.py:73-79].
