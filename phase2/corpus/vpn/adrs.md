# vpn — retro-ADRs (NetBox @ ea4c205)

Decisions the code embodies but nobody wrote down, stated as the code has them [fg:subsystems:vpn].

## ADR-1. L2VPN was moved from ipam into vpn without touching the database tables

**Context.** L2VPN and L2VPNTermination originally lived in `ipam` (their tables and constraints still carry `ipam_l2vpn_*` names in the rename SQL) [code:netbox/vpn/migrations/0005_rename_indexes.py:9-20]. When the `vpn` app was created (first commits 2023-11-27) the L2VPN models were relocated into it [fg:churn:vpn.models.l2vpn] [fg:churn:vpn.migrations.0001_initial].

**Decision.** The move is a pure state migration: `vpn.0002_move_l2vpn` wraps `CreateModel` in `SeparateDatabaseAndState` with `database_operations=[]`, depending on `ipam.0068_move_l2vpn` which removes the models from ipam's state and rewrites the existing ContentType rows' `app_label` from `ipam` to `vpn` in place so every GFK, tag and changelog row keeps pointing at the same content type ids [code:netbox/vpn/migrations/0002_move_l2vpn.py:8-19] [code:netbox/vpn/migrations/0002_move_l2vpn.py:95-97] [code:netbox/ipam/migrations/0068_move_l2vpn.py:4-14]. Leftover physical names were fixed later with raw `ALTER ... RENAME` statements in 0005 [code:netbox/vpn/migrations/0005_rename_indexes.py:9-20].

**Consequences.** vpn's migration graph is permanently entangled with ipam (0001 depends on `ipam.0054_squashed_0067`, 0002 on `ipam.0068_move_l2vpn`, 0003 on `ipam.0069_gfk_indexes`) [code:netbox/vpn/migrations/0001_initial.py:10-14] [code:netbox/vpn/migrations/0003_ipaddress_multiple_tunnel_terminations.py:8-11]. The L2VPNTermination unique-constraint name is hard-coded as `vpn_l2vpntermination_assigned_object` rather than the `%(app_label)s_%(class)s_...` template the tunnel models use, because it had to match an already-renamed constraint [code:netbox/vpn/models/l2vpn.py:111-116] [code:netbox/vpn/models/tunnels.py:141-147]. ipam, dcim and virtualization still import L2VPN back from vpn for filters and nested serializers, so the dependency direction is now ipam → vpn for this model family [fg:imports:ipam.filtersets->vpn.models] [fg:imports:ipam.api.serializers_.vlans->vpn.api.serializers_.l2vpn].

## ADR-2. Tunnel and L2VPN endpoints are modelled as separate termination rows with a GenericForeignKey, not as FKs on the endpoint objects

**Context.** A tunnel or L2VPN can attach to a device interface, a VM interface, or (for L2VPN) a VLAN; the set of endpoint types is open across three apps [code:netbox/vpn/constants.py:3-7] [code:netbox/vpn/choices.py:46-54].

**Decision.** Each attachment is its own row (TunnelTermination, L2VPNTermination) holding a ContentType FK plus object id, and the endpoint apps declare the reverse `GenericRelation` [code:netbox/vpn/models/tunnels.py:114-126] [code:netbox/vpn/models/l2vpn.py:93-102] [fg:model_refs:dcim.models.device_components:781] [fg:model_refs:ipam.models.vlans:246]. vpn holds no FK to dcim or virtualization at all; its only cross-app model FKs are to ipam.IPAddress, ipam.RouteTarget and tenancy.Tenant [fg:model_refs:vpn.models.tunnels:127] [fg:model_refs:vpn.models.l2vpn:46] [fg:model_refs:vpn.models.l2vpn:56].

**Consequences.** Every layer must re-derive the concrete type: forms swap querysets on a `type` switch, filtersets join through the target apps' `related_query_name`s, REST uses a method field with `get_serializer_for_model`, GraphQL declares a union [code:netbox/vpn/forms/model_forms.py:273-283] [code:netbox/vpn/filtersets.py:450-458] [code:netbox/vpn/api/serializers_/l2vpn.py:65-69] [code:netbox/vpn/graphql/types.py:151-157]. The endpoint side exposes convenience accessors (`tunnel_termination`, `l2vpn_termination`) that vpn's own `clean()` depends on [code:netbox/dcim/models/device_components.py:624-625] [code:netbox/vpn/models/tunnels.py:164]. Termination tables cannot order by the generic columns (`orderable=False`), and a regression test exists to catch ordering exceptions [code:netbox/vpn/tables/tunnels.py:84-94] [code:netbox/vpn/tests/test_tables.py:7-23].

## ADR-3. An endpoint object may belong to at most one tunnel and one L2VPN — enforced by a DB constraint and again in `clean()`

**Context.** Generic FKs have no database-level referential integrity, and the UI needs an error on the right field rather than an IntegrityError [code:netbox/vpn/models/l2vpn.py:126].

**Decision.** Both termination models declare `UniqueConstraint(fields=(type, id))` and duplicate the check in `clean()` [code:netbox/vpn/models/tunnels.py:141-147] [code:netbox/vpn/models/tunnels.py:160-170] [code:netbox/vpn/models/l2vpn.py:111-116] [code:netbox/vpn/models/l2vpn.py:125-136]. The tunnel constraint carries a `violation_error_message` for the DB path too [code:netbox/vpn/migrations/0001_initial.py:305-311].

**Consequences.** The separate `(type, id)` indexes added in 0001 and 0002 were later judged redundant and removed in 0009 [code:netbox/vpn/migrations/0001_initial.py:301-304] [code:netbox/vpn/migrations/0009_remove_redundant_indexes.py:13-20]. The test suite covers the L2VPN half only [code:netbox/vpn/tests/test_models.py:63-79].

## ADR-4. IPSec parameters are a five-model reference hierarchy, attached to Tunnel by a single optional FK

**Context.** IKE and IPSec each have proposals (algorithm sets) and policies (ordered proposal lists plus version/PFS settings); a profile pairs one of each [code:netbox/vpn/models/crypto.py:17-19] [code:netbox/vpn/models/crypto.py:122-124].

**Decision.** Five separate PrimaryModels, all first-class (own views, API, search, changelog), with M2M `proposals` on each policy, PROTECT FKs from IPSecProfile to both policies, and Tunnel.ipsec_profile nullable [fg:model_refs:vpn.models.crypto:85] [fg:model_refs:vpn.models.crypto:185] [fg:model_refs:vpn.models.crypto:225] [fg:model_refs:vpn.models.crypto:230] [code:netbox/vpn/models/tunnels.py:55-61]. Business rules that cross fields live in `clean()`: IKEv1 requires mode and IKEv2 forbids it; an IPSec proposal must set at least one algorithm [code:netbox/vpn/models/crypto.py:110-119] [code:netbox/vpn/models/crypto.py:170-175].

**Consequences.** A tunnel of any encapsulation may reference an IPSec profile; nothing ties `ipsec_profile` to the IPSec encapsulation choices [code:netbox/vpn/choices.py:24-43] [code:netbox/vpn/models/tunnels.py:50-61]. Deleting a proposal in use is blocked by PROTECT semantics up the chain, so `prerequisite_models` is declared on each dependent model to drive the UI [code:netbox/vpn/models/crypto.py:98-100] [code:netbox/vpn/models/crypto.py:239-242]. The pre-shared key is stored in plain text as an ordinary TextField and is exposed as a filterable field [code:netbox/vpn/models/crypto.py:90-93] [code:netbox/vpn/filtersets.py:184].

## ADR-5. Tunnel creation is a two-termination wizard implemented as a form subclass, not a separate view

**Context.** Most tunnels are point-to-point, so creating a tunnel and its two ends in one step is the common case [code:netbox/vpn/forms/model_forms.py:75] [code:netbox/vpn/forms/model_forms.py:110].

**Decision.** TunnelCreateForm extends TunnelForm with `termination1_*` and `termination2_*` field groups and creates TunnelTermination rows in `save()`; TunnelEditView swaps to it in `dispatch()` only when no `pk` is present, so the registered `add`/`edit` view pair is unchanged [code:netbox/vpn/forms/model_forms.py:74-108] [code:netbox/vpn/forms/model_forms.py:145-155] [code:netbox/vpn/forms/model_forms.py:201-222] [code:netbox/vpn/views.py:89-101]. Termination type is a dedicated ChoiceSet (`dcim.device` / `virtualization.virtualmachine`) used only by these forms [code:netbox/vpn/choices.py:46-54].

**Consequences.** The termination sub-forms are hand-duplicated rather than a formset, and the cross-field validation in `clean()` only runs against the second block because the check sits outside the loop [code:netbox/vpn/forms/model_forms.py:182-199]. Terminations created this way are not run through TunnelTerminationForm's validation path [code:netbox/vpn/forms/model_forms.py:204-220].

## ADR-6. L2VPN "point-to-point" types are capped at two terminations by a class-level tuple and model validation

**Context.** Some L2VPN types (VPWS, EPL, EP-LAN, EP-Tree) are semantically two-ended [code:netbox/vpn/choices.py:264-269].

**Decision.** `L2VPNTypeChoices.P2P` lists those types; L2VPNTermination.clean() refuses a third termination, and L2VPN exposes `can_add_termination` for the UI [code:netbox/vpn/models/l2vpn.py:138-147] [code:netbox/vpn/models/l2vpn.py:79-84].

**Consequences.** The rule is not a DB constraint, so bulk_create and API bypasses of `clean()` can exceed it. Changing an L2VPN's `type` after it has three terminations is not validated on the L2VPN side, which defines no `clean()` [code:netbox/vpn/models/l2vpn.py:66-84]. `can_add_termination` is a `cached_property`, so it goes stale within one instance's lifetime [code:netbox/vpn/models/l2vpn.py:79-80].

## ADR-7. Each termination row logs changes against its parent, and TunnelTermination is a ChangeLoggedModel rather than a NetBoxModel

**Context.** A termination is subordinate to its tunnel; changelog readers want to see it under the tunnel [code:netbox/vpn/models/tunnels.py:172-175].

**Decision.** TunnelTermination inherits ChangeLoggedModel plus CustomFieldsMixin, CustomLinksMixin and TagsMixin — explicitly not the full NetBoxModel feature set — and overrides `to_objectchange` to set `related_object = self.tunnel` [fg:symbols:vpn.models.tunnels:TunnelTermination] [code:netbox/vpn/models/tunnels.py:102] [code:netbox/vpn/models/tunnels.py:172-175]. L2VPNTermination, by contrast, is a full NetBoxModel with no such override [fg:symbols:vpn.models.l2vpn:L2VPNTermination] [code:netbox/vpn/models/l2vpn.py:87].

**Consequences.** The two termination models diverge in features (e.g. GraphQL type for TunnelTermination composes CustomFieldsMixin/TagsMixin on plain ObjectType while L2VPNTerminationType is a NetBoxObjectType) and in search indexing (neither is indexed) [code:netbox/vpn/graphql/types.py:49] [code:netbox/vpn/graphql/types.py:148] [fg:modules:vpn.search] [code:netbox/vpn/search.py:5-14]. TunnelTermination still needs an explicit `get_absolute_url` because that default lives on NetBoxFeatureSet, which ChangeLoggedModel does not include [code:netbox/vpn/models/tunnels.py:154-155] [code:netbox/netbox/models/__init__.py:25-46] [code:netbox/netbox/models/__init__.py:53].

## ADR-8. Optional choice fields store NULL, and unbounded CharFields drop `max_length`

**Context.** Filtering on "no value" needs NULL, not empty string; migration 0004 first made IKEPolicy.mode `blank=True` and 0006 then made it and three algorithm fields nullable with a data fix [code:netbox/vpn/migrations/0004_alter_ikepolicy_mode.py:12-17] [code:netbox/vpn/migrations/0006_charfield_null_choices.py:4-16].

**Decision.** Those fields are `CharField(blank=True, null=True)` without `max_length` [code:netbox/vpn/models/crypto.py:36-41] [code:netbox/vpn/models/crypto.py:79-84]. The required choice fields on the same models also omit `max_length` [code:netbox/vpn/models/crypto.py:28-35] [code:netbox/vpn/models/crypto.py:221-224].

**Consequences.** Tunnel and L2VPN, written earlier, keep `max_length=50` on their choice fields, so the app has two conventions side by side [code:netbox/vpn/models/tunnels.py:37-42] [code:netbox/vpn/models/l2vpn.py:30-40].

## ADR-9. Every `name` gets `natural_sort` collation and global uniqueness

**Context.** Names like "Tunnel 10" should sort after "Tunnel 9"; dcim introduced the collation in `0197_natural_sort_collation` [code:netbox/vpn/migrations/0007_natural_ordering.py:5-8].

**Decision.** Migration 0007 altered all seven `name` fields to `db_collation='natural_sort'`, matching the model declarations [code:netbox/vpn/migrations/0007_natural_ordering.py:11-45] [code:netbox/vpn/models/crypto.py:22-27].

**Consequences.** vpn's migration chain now also depends on dcim [code:netbox/vpn/migrations/0007_natural_ordering.py:5-8]. Tunnel's group-scoped uniqueness constraints are dead weight under the global `unique=True` [code:netbox/vpn/models/tunnels.py:31-36] [code:netbox/vpn/models/tunnels.py:81-91].
