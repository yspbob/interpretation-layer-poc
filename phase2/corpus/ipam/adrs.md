# ipam — retro-ADRs (NetBox @ ea4c205)

## ADR-1: Native PostgreSQL `cidr`/`inet` columns with netaddr objects and hand-written lookups

**Context.** Prefix/IP hierarchy questions ("what contains X", "what is inside Y", "same host, any mask") must run as database filters over potentially large tables, and Django has no built-in containment operators for network types. [code:netbox/ipam/lookups.py:143-154] [code:netbox/ipam/models/ip.py:376-405]

**Decision.** `IPNetworkField.db_type` is `cidr`, `IPAddressField.db_type` is `inet`, both always deserialise to `netaddr.IPNetwork`; 19 custom `Lookup`/`Transform` classes emit PostgreSQL operators (`>>`, `<<`, `<<=`, `HOST()`, `FAMILY()`, `MASKLEN()`) and are registered on the fields at import. [code:netbox/ipam/fields.py:21-64] [code:netbox/ipam/fields.py:67-109] [code:netbox/ipam/lookups.py:49-100]

**Consequences.** The subsystem is PostgreSQL-only; callers must stringify netaddr values before filtering; text lookups need `TEXT()` wrapping and `NetHost` must strip the mask from its parameter; sane IP ordering needs a manager-level `INET(HOST(address))` order plus a functional index; the hierarchy annotation drops to `RawSQL` naming the `ipam_prefix` table. [code:netbox/ipam/lookups.py:4-10] [code:netbox/ipam/lookups.py:95-100] [code:netbox/ipam/managers.py:9-17] [code:netbox/ipam/models/ip.py:794-797] [code:netbox/ipam/querysets.py:37-57]

**Evidence.** The lookup module has 16 commits across nine years and `managers.py` none since 2020, so this layer is settled. [fg:churn:ipam.lookups] [fg:churn:ipam.managers]

## ADR-2: Prefix depth and child counts are materialised, maintained by signals, repairable by command

**Context.** Prefix tables render depth indentation and child counts for every row; computing containment per row on read is a query per prefix. [code:netbox/ipam/tables/template_code.py:17-25] [code:netbox/ipam/tables/ip.py:157-171]

**Decision.** `Prefix._depth` and `_children` are non-editable columns; `Prefix.__init__` caches the original prefix and VRF, and `post_save`/`post_delete` receivers recompute parents' child counts and children's depths (for both the new and old location on change) with `annotate_hierarchy()` and `bulk_update`; a stack-based `rebuild_prefixes()` and management command rebuild everything per VRF. [code:netbox/ipam/models/ip.py:259-267] [code:netbox/ipam/models/ip.py:280-285] [code:netbox/ipam/signals.py:9-49] [code:netbox/ipam/utils.py:191-248] [code:netbox/ipam/management/commands/rebuild_prefixes.py:10-27]

**Consequences.** Every Prefix create/move/delete costs two annotated queries and bulk updates over the affected subtree; anything that writes prefixes without firing model signals (queryset `update`, raw loads) leaves stale counts until the command runs; `hierarchy_depth`/`hierarchy_children` compare VRFs with `COALESCE(vrf_id, 0)` because NULL != NULL. [code:netbox/ipam/signals.py:29-42] [code:netbox/ipam/querysets.py:37-57] [code:netbox/ipam/management/commands/rebuild_prefixes.py:13-14]

**Evidence.** `TestPrefixHierarchy` covers create/update/VRF-move/delete/duplicate for v4 and v6; migration 0072 added cached relations. [code:netbox/ipam/tests/test_models.py:336-359] [fg:modules:ipam.migrations.0072_prefix_cached_relations]

## ADR-3: Uniqueness of IP space is a per-VRF policy enforced in `clean()`, never a database constraint

**Context.** Real networks legitimately duplicate space across VRFs and duplicate host addresses for anycast/VIP/FHRP roles, so a hard unique index on (vrf, prefix) or (vrf, address) would reject valid data. [code:netbox/ipam/constants.py:40-48] [code:netbox/ipam/models/ip.py:709-719]

**Decision.** `vrf=None` denotes the global table; `VRF.enforce_unique` defaults to True and the global table follows `ENFORCE_GLOBAL_UNIQUE`; `Prefix.clean` and `IPAddress.clean` call `get_duplicates()` and raise only when the applicable flag is set; `Meta.ordering` on Prefix/IPRange/IPAddress includes `pk` with a "may be non-unique" comment and no `UniqueConstraint` is declared. [code:netbox/ipam/models/vrfs.py:39-43] [code:netbox/ipam/models/ip.py:302-311] [code:netbox/ipam/models/ip.py:875-887] [code:netbox/ipam/models/ip.py:275-278] [code:netbox/ipam/models/ip.py:792-799]

**Consequences.** Uniqueness holds only on code paths that run `clean()`; duplicate rows are a first-class UI concept (duplicate tables on Prefix and IPAddress detail views); container prefixes in the global table deliberately see children from every VRF. [code:netbox/ipam/views.py:538-551] [code:netbox/ipam/views.py:807-821] [code:netbox/ipam/models/ip.py:381-384] [code:netbox/ipam/models/ip.py:402-405]

**Evidence.** `TestPrefix` and `TestIPAddress` each carry global/VRF × unique/non-unique duplicate cases plus role-exemption cases. [code:netbox/ipam/tests/test_models.py:313-334] [code:netbox/ipam/tests/test_models.py:551-590]

## ADR-4: Polymorphic assignment via GenericForeignKey bounded by `Q` constants, migrated away from concrete FKs

**Context.** Several ipam objects attach to more than one kind of parent (IPAddress → Interface/VMInterface/FHRPGroup; Service → Device/VM/FHRPGroup; VLANGroup → seven scope types; Prefix → four location types). Earlier schemas used concrete FKs: Service had `device`/`virtual_machine`, Prefix had `site`, and L2VPN lived in ipam. [code:netbox/ipam/migrations/0080_populate_service_parent.py:6-21] [code:netbox/ipam/migrations/0071_prefix_scope.py:6-18] [code:netbox/ipam/migrations/0068_move_l2vpn.py:4-14]

**Decision.** Each GFK is paired with a `Q` over `(app_label, model)` in `constants.py`, a composite `(type, id)` index, serializer `ContentTypeField(queryset=ContentType.objects.filter(Q))`, and an HTMX-driven form pair; migrations copy old FK values into the GFK and ship `objectchange_migrators` to rewrite historical change-log payloads. [code:netbox/ipam/constants.py:31-35] [code:netbox/ipam/constants.py:86-90] [code:netbox/ipam/models/services.py:67-95] [code:netbox/ipam/api/serializers_/ip.py:166-170] [code:netbox/ipam/migrations/0080_populate_service_parent.py:60-80] [code:netbox/ipam/migrations/0071_prefix_scope.py:50-64]

**Consequences.** Adding an assignable type means touching the constant, the serializer, the form, the filterset's per-type convenience filters, the GraphQL union, and the `GenericPrefetch` list in `IPAddressViewSet` in lockstep; scope-aware VLAN lookup requires the hand-built `VLANQuerySet.get_for_site/device/virtualmachine` walking ancestors per scope type; `VLAN.site` survives alongside group scope and must be cross-validated in `VLAN.clean`. [code:netbox/ipam/api/views.py:106-116] [code:netbox/ipam/filtersets.py:738-771] [code:netbox/ipam/graphql/types.py:155-161] [code:netbox/ipam/querysets.py:102-141] [code:netbox/ipam/models/vlans.py:288-302]

**Evidence.** Migrations 0068, 0071, 0079–0081 and their cross-app `get_model` references. [fg:model_refs:ipam.migrations.0080_populate_service_parent:9] [fg:model_refs:ipam.migrations.0071_prefix_scope:12] [fg:model_refs:ipam.migrations.0068_move_l2vpn:5]

## ADR-5: "Next available" allocation is a dedicated API view family serialised by PostgreSQL advisory locks

**Context.** Concurrent clients asking for the next free IP/prefix/VLAN/ASN must not receive the same answer, and availability is computed in Python from an `IPSet`, not by the database. [code:netbox/ipam/models/ip.py:407-437] [code:netbox/ipam/models/vlans.py:139-150]

**Decision.** `AvailableObjectsView` (an `APIView`, not a viewset action) computes availability inside `advisory_lock(ADVISORY_LOCK_KEYS[...])`, returns 409 when insufficient, then writes through the model's normal serializer inside `transaction.atomic`; `IPAddressViewSet.create/update/destroy` take the same `available-ips` lock; routes are explicit paths beside the router. [code:netbox/ipam/api/views.py:253-304] [code:netbox/ipam/api/views.py:120-130] [code:netbox/ipam/api/urls.py:31-57] [code:netbox/netbox/constants.py:10-15]

**Consequences.** One global key per object type serialises all API IP writes, not just allocations; the UI create path (`IPAddressEditView`, `IPAddressForm`) does not take the lock, so UI and API allocations are not mutually excluded; GET listings are capped by `get_results_limit` and available IPs are produced by iterating the `IPSet` up to that limit; write serializers diverge from model serializers (`PrefixLengthSerializer`, `CreateAvailableVLANSerializer` skipping validation). [code:netbox/ipam/views.py:1-24] [code:netbox/ipam/views.py:829-834] [code:netbox/ipam/api/views.py:187-199] [code:netbox/ipam/api/views.py:406-413] [code:netbox/ipam/api/serializers_/ip.py:85-109] [code:netbox/ipam/api/serializers_/vlans.py:116-118]

**Evidence.** `api/views.py` is the second most-changed non-test module (144 commits, last 2025-06-25). [fg:churn:ipam.api.views]

## ADR-6: Free space is rendered as unsaved placeholder rows inside the real object tables

**Context.** Operators want to see gaps between prefixes, IPs and VLAN IDs inline and click through to create them. [code:netbox/ipam/tables/template_code.py:5-11] [code:netbox/ipam/views.py:587-593]

**Decision.** `prep_table_data()` injects placeholders (`Prefix(prefix=p, status=None)`, `AvailableIPSpace`, VLAN dicts) only when the request has no search and no explicit ordering; templates test `record.pk`, and `PrefixUtilizationColumn` renders nothing for pk-less rows. [code:netbox/ipam/views.py:580-585] [code:netbox/ipam/views.py:641-644] [code:netbox/ipam/views.py:1036-1039] [code:netbox/ipam/utils.py:36-63] [code:netbox/ipam/utils.py:177-188] [code:netbox/ipam/tables/ip.py:142-154]

**Consequences.** Tables and templates must tolerate heterogeneous row types; sorting or searching silently hides availability; `AvailableIPSpace.title` collapses anything above 65,536 to "Many IPs available", and IPRange size is capped at 2^32−1 at validation time. [code:netbox/ipam/utils.py:27-33] [code:netbox/ipam/models/ip.py:602-607]

**Evidence.** `views.py` has 401 commits from 26 authors and `tables/ip.py` 69 from 16, consistent with this presentation logic absorbing sustained change. [fg:churn:ipam.views] [fg:churn:ipam.tables.ip]
