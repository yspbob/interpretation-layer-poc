# circuits — retro-ADRs (NetBox @ ea4c205)

Decisions the code embodies but nobody wrote down; each is stated as the code has it today, for the subsystem summarised in the fact graph. [fg:subsystems:circuits]

## ADR-C1: A circuit termination points at its far end through a GenericForeignKey with a closed allowlist

**Context.** Until migration 0047, CircuitTermination had two nullable FKs, `site` and `provider_network`; a termination ended at one or the other. Regions, site groups and locations could not be termination points. [code:netbox/circuits/migrations/0047_circuittermination__termination.py:6-23]

**Decision.** Replace the pair of FKs with `termination_type`/`termination_id`/`termination` (a GFK), and constrain the allowed target models to a fixed tuple in `constants.py` (`region`, `sitegroup`, `site`, `location`, `providernetwork`). The tuple is re-applied as a ContentType queryset in every writable surface (model form, bulk-edit form, import form, REST serializer) and the GraphQL union enumerates the same five types. [code:netbox/circuits/models/circuits.py:248-262] [code:netbox/circuits/constants.py:5-7] [code:netbox/circuits/forms/model_forms.py:167-172] [code:netbox/circuits/api/serializers_/circuits.py:126-133] [code:netbox/circuits/graphql/types.py:79-87]

**Consequences.** A termination with no target is invalid (`clean()` enforces it), so the GFK is effectively required although both columns are nullable. Adding a new target model means editing the constant, `cache_related_objects()`, and the GraphQL union together. Old change-log records are rewritten by an `objectchange_migrators` hook so history stays readable. [code:netbox/circuits/models/circuits.py:347-351] [code:netbox/circuits/models/circuits.py:359-378] [code:netbox/circuits/migrations/0047_circuittermination__termination.py:55-75]

## ADR-C2: Filterability is bought with denormalised cache FKs, recomputed on save

**Context.** A GFK cannot be joined or filtered by region/site/location, and dcim's Region/SiteGroup/Site/Location pages need "circuits here" lists. [code:netbox/dcim/views.py:240-262]

**Decision.** Migration 0048 adds `_location`, `_region`, `_site`, `_site_group` and renames `provider_network` to `_provider_network`; `CircuitTermination.save()` rebuilds all five from the GFK target, walking up (location→site→region/group). Filtersets, tables, dcim views and the cable-path tracer all read these fields, never the GFK. [code:netbox/circuits/migrations/0048_circuitterminations_cached_relations.py:31-88] [code:netbox/circuits/models/circuits.py:353-378] [code:netbox/circuits/filtersets.py:280-334] [code:netbox/dcim/models/cables.py:699-705]

**Consequences.** The cache FKs use `on_delete=CASCADE`, so deleting a Site, Region, SiteGroup or Location deletes every termination cached against it, even though the GFK's ContentType FK is PROTECT. Any code that changes a termination's target without calling `save()` (e.g. `QuerySet.update`) leaves stale caches. Circuit-level filters (`terminations___region`) and Provider-level filters (`circuits__terminations___region`) are two-hop joins through the cache. [code:netbox/circuits/models/circuits.py:301-328] [code:netbox/circuits/filtersets.py:33-38] [code:netbox/circuits/filtersets.py:200-205]

## ADR-C3: Circuit keeps non-editable pointers to its A and Z terminations, maintained by a signal

**Context.** Circuit list pages and serializers show both ends on every row; joining `terminations` and picking by side is awkward and slow. [code:netbox/circuits/tables/circuits.py:68-77]

**Decision.** `Circuit.termination_a` and `termination_z` are `editable=False`, `SET_NULL` FKs. A `post_save` receiver on CircuitTermination refreshes the circuit and writes the termination into the matching slot. The (circuit, term_side) unique constraint guarantees at most one per side. The API exposes them read-only through a dedicated `CircuitCircuitTerminationSerializer`. [code:netbox/circuits/models/circuits.py:96-112] [code:netbox/circuits/signals.py:8-15] [code:netbox/circuits/models/circuits.py:332-337] [code:netbox/circuits/api/serializers_/circuits.py:109-110]

**Consequences.** Swapping ends cannot be done by editing the circuit; `CircuitSwapTerminations` re-saves the terminations inside a transaction with a temporary `'_'` side to avoid tripping the unique constraint, then fixes the pointers by hand. There is no `post_delete` receiver clearing the slot; `SET_NULL` on the FK does that at the database level. [code:netbox/circuits/views.py:385-409] [code:netbox/circuits/models/circuits.py:97-104]

## ADR-C4: Physical circuit terminations are cable endpoints, and dcim path tracing hops through circuits

**Context.** Circuits carry cabled connectivity between sites; a trace from an interface should continue across the carrier to the far site. [code:netbox/dcim/models/cables.py:694-697]

**Decision.** CircuitTermination inherits dcim's `CabledObjectModel`, its filterset inherits `CabledObjectFilterSet`, its API viewset mixes in `PassThroughPortMixin`, and dcim's `PathTraceView` is registered on it. dcim's `CablePath.from_origin` follows a CircuitTermination to its opposite side, stopping if that side is on a provider network. When a termination is saved or deleted, `rebuild_cablepaths` asks dcim to rebuild paths through the peer. A termination whose target is a ProviderNetwork may not be cabled at all. [code:netbox/circuits/models/circuits.py:231-237] [code:netbox/circuits/filtersets.py:270] [code:netbox/circuits/api/views.py:52] [code:netbox/circuits/views.py:476] [code:netbox/circuits/signals.py:18-27] [code:netbox/dcim/models/cables.py:344-346]

**Consequences.** circuits and dcim are mutually dependent: dcim imports `circuits.models` lazily inside functions to break the cycle. `get_peer_termination()` exists on the model specifically to serve the signal. Changes to termination sides or targets can trigger CablePath recomputation in dcim. [code:netbox/dcim/models/cables.py:529] [code:netbox/circuits/models/circuits.py:389-397] [fg:imports:dcim.models.cables->circuits.models]

## ADR-C5: Virtual circuits are a separate model family, not a flag on Circuit

**Context.** Virtual circuits (e.g. L2VPN-style services over a carrier network) terminate on device interfaces, not on sites, and have no A/Z, cabling, distance or install dates. [code:netbox/circuits/models/virtual_circuits.py:32-35]

**Decision.** Migration 0050 creates VirtualCircuitType, VirtualCircuit and VirtualCircuitTermination. A VirtualCircuit belongs to a ProviderNetwork (its `provider` is derived), may carry a ProviderAccount validated against that provider, and shares `CircuitStatusChoices`. A termination is a `OneToOneField` to a dcim Interface that must be virtual, with a role of peer, hub or spoke, and `peer_terminations` is computed from the role. The type models share `BaseCircuitType` only for the `color` field. [fg:modules:circuits.migrations.0050_virtual_circuits] [code:netbox/circuits/models/virtual_circuits.py:41-70] [code:netbox/circuits/models/virtual_circuits.py:116-118] [code:netbox/circuits/models/virtual_circuits.py:138-142] [code:netbox/circuits/models/virtual_circuits.py:172-191] [code:netbox/circuits/models/base.py:11-23]

**Consequences.** Every layer is duplicated rather than parameterised (forms, tables, filtersets, serializers, GraphQL, views, tests), and the duplication carried over vestiges that do not fit: cabled-object API mixins and contacts columns on models that have neither. Provider-scoped queries must union both families explicitly. [code:netbox/circuits/api/serializers_/circuits.py:209] [code:netbox/circuits/tables/virtual_circuits.py:39] [code:netbox/circuits/views.py:36-51] [code:netbox/circuits/filtersets.py:453-468]

## ADR-C6: Circuit group membership is a GenericForeignKey limited to the two circuit models

**Context.** Circuit groups (0044) originally held Circuits by a plain FK with a (circuit, group) uniqueness rule. Virtual circuits needed grouping too. [code:netbox/circuits/migrations/0044_circuit_groups.py:82-84]

**Decision.** Migration 0051 renames `circuit` to `member_id`, adds `member_type`, back-fills the Circuit content type, and swaps the unique constraint for (member_type, member_id, group). `CIRCUIT_GROUP_ASSIGNMENT_MEMBER_MODELS` restricts the type to `circuit` and `virtualcircuit`; both models declare a `GenericRelation` so `assignments` is reachable from either side. [code:netbox/circuits/migrations/0051_virtualcircuit_group_assignment.py:28-85] [code:netbox/circuits/constants.py:9-12] [code:netbox/circuits/models/circuits.py:114-119] [code:netbox/circuits/models/virtual_circuits.py:72-77]

**Consequences.** Filtering assignments by circuit, virtual circuit or provider is done with method filters that resolve content types and `member_id__in` subqueries, since no join exists; the search filter's `member__cid` relies on the related_query_name. The serializer used inside `CircuitSerializer.assignments` is a trimmed base class (`CircuitGroupAssignmentSerializer_`) without the member fields to avoid recursion. [code:netbox/circuits/filtersets.py:431-468] [code:netbox/circuits/filtersets.py:423-429] [code:netbox/circuits/api/serializers_/circuits.py:87-99]

## ADR-C7: Nested terminations are imported with the parent, via a form triplet and extra permissions

**Context.** Importing a circuit without its ends is rarely useful; a two-pass import is error-prone. [code:netbox/circuits/tests/test_views.py:199-221]

**Decision.** Both `CircuitBulkImportView` and `VirtualCircuitBulkImportView` declare `related_object_forms={'terminations': ...ImportRelatedForm}`, require the `add_<termination>` permission in addition to `add_<circuit>`, and inject the parent through `prep_related_object_data`. The related form is a plain `ModelForm` sharing a base with the standalone import form so field definitions are written once. [code:netbox/circuits/views.py:314-327] [code:netbox/circuits/views.py:676-688] [code:netbox/circuits/forms/bulk_import.py:126-165] [code:netbox/circuits/forms/bulk_import.py:247-280]

**Consequences.** The related form omits `tags` and the NetBox import mixin, so nested terminations cannot be tagged on import; the standalone form can. A dedicated test guards each path. [code:netbox/circuits/forms/bulk_import.py:143-152] [code:netbox/circuits/forms/bulk_import.py:155-165] [code:netbox/circuits/tests/test_views.py:701-750]

## ADR-C8: Provider accounts and provider networks are first-class objects scoped under Provider

**Context.** A carrier relationship spans several billing accounts and several opaque external networks; circuits and virtual circuits must reference these consistently. [code:netbox/circuits/models/providers.py:49-52] [code:netbox/circuits/models/providers.py:92-96]

**Decision.** ProviderAccount and ProviderNetwork are `PrimaryModel`s with FK to Provider (PROTECT), unique per provider by `account`/`name`, with a conditional uniqueness on account `name` only when non-empty. Circuit.provider_account is optional and validated to match `provider`; VirtualCircuit reaches its provider only through ProviderNetwork. Provider and ProviderNetwork names use the `natural_sort` collation (0049). [code:netbox/circuits/models/providers.py:53-57] [code:netbox/circuits/models/providers.py:72-82] [code:netbox/circuits/models/providers.py:113-120] [code:netbox/circuits/models/circuits.py:151-155] [code:netbox/circuits/migrations/0049_natural_ordering.py:11-20]

**Consequences.** Circuit uniqueness is enforced twice, per provider and per account, so the same `cid` can exist under two providers but not under two accounts of one provider. Provider serializers embed accounts via a `WritableNestedSerializer` and ASNs from ipam, making `ProviderSerializer` the one place circuits depends on ipam's API layer. [code:netbox/circuits/models/circuits.py:132-141] [code:netbox/circuits/api/serializers_/providers.py:17-30] [fg:imports:circuits.api.serializers_.providers->ipam.api.serializers_.asns]
