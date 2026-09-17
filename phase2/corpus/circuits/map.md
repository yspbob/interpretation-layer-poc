# circuits — subsystem map (NetBox @ ea4c205)

## What it is

`circuits` is the Django app that models carrier-provided connectivity: Providers, their accounts and external networks, physical Circuits with A/Z terminations, Virtual Circuits with role-based terminations, and Circuit Groups that collect either kind of circuit. It is 44 non-test modules, 8,214 lines of code, and 5 test modules. [fg:subsystems:circuits]

Eleven concrete models are exported: Provider, ProviderAccount, ProviderNetwork (providers.py); CircuitType, Circuit, CircuitGroup, CircuitGroupAssignment, CircuitTermination (circuits.py); VirtualCircuitType, VirtualCircuit, VirtualCircuitTermination (virtual_circuits.py). One abstract base, BaseCircuitType, carries the shared `color` field for the two type models. [fg:symbols:circuits.models.base:BaseCircuitType] [code:netbox/circuits/models/__init__.py:1-3]

## Modules by role

**Models.** `models/circuits.py` (398 loc) is the core: Circuit is a PrimaryModel with Contacts, ImageAttachments and Distance mixins; CircuitTermination is a ChangeLoggedModel that is also a dcim `CabledObjectModel`; CircuitGroupAssignment is a ChangeLoggedModel with a GenericForeignKey `member`. [fg:modules:circuits.models.circuits] [code:netbox/circuits/models/circuits.py:38] [code:netbox/circuits/models/circuits.py:231-237]

`models/providers.py` (126 loc) holds Provider (unique natural-sort name, M2M to ipam.ASN), ProviderAccount and ProviderNetwork, both FK'd to Provider with per-provider unique constraints. [fg:modules:circuits.models.providers] [code:netbox/circuits/models/providers.py:20-36] [code:netbox/circuits/models/providers.py:70-82]

`models/virtual_circuits.py` (192 loc) holds VirtualCircuit (FK to ProviderNetwork, not Provider; `provider` is a derived property) and VirtualCircuitTermination (OneToOne to dcim.Interface, role peer/hub/spoke). [fg:modules:circuits.models.virtual_circuits] [code:netbox/circuits/models/virtual_circuits.py:116-118] [code:netbox/circuits/models/virtual_circuits.py:138-142]

**Choices and constants.** `choices.py` defines six ChoiceSets (status, commit rate, termination side, port speed, group priority, virtual termination role); `constants.py` defines the allowed termination-type model names and the Q filter for group-assignment member models. Both are consumed by models, forms, serializers and filtersets. [fg:modules:circuits.choices] [code:netbox/circuits/constants.py:5-12] [fg:imports:circuits.api.serializers_.circuits->circuits.constants]

**Views and URLs.** `views.py` (751 loc, 78 classes) is one class per model per action (List/View/Edit/Delete/BulkImport/BulkEdit/BulkDelete) plus the bespoke `CircuitSwapTerminations` and a registration of dcim's `PathTraceView` for terminations. `urls.py` wires most models via `get_model_urls`, with explicit paths only for the swap view and the virtual-circuit list/bulk views. [fg:modules:circuits.views] [code:netbox/circuits/views.py:349-353] [code:netbox/circuits/views.py:476] [code:netbox/circuits/urls.py:20-26] [code:netbox/circuits/urls.py:37-43]

**Forms.** Four modules under `forms/`: `model_forms.py` (11 forms), `bulk_edit.py` (11), `bulk_import.py` (15, including Base/Related/full triplets for both termination kinds), `filtersets.py` (11). [fg:modules:circuits.forms.model_forms] [fg:modules:circuits.forms.bulk_import] [code:netbox/circuits/forms/bulk_import.py:126-165]

**Tables.** `tables/circuits.py`, `tables/providers.py`, `tables/virtual_circuits.py`, plus `tables/columns.py` with the single custom `CommitRateColumn`. [fg:modules:circuits.tables.circuits] [fg:symbols:circuits.tables.columns:CommitRateColumn]

**Filtersets.** `filtersets.py` (591 loc) — one FilterSet per model, built on `NetBoxModelFilterSet`/`OrganizationalModelFilterSet` with Tenancy, Contact and CabledObject mixins from other apps. [fg:modules:circuits.filtersets] [code:netbox/circuits/filtersets.py:6-10]

**REST API.** `api/views.py` is 11 `NetBoxModelViewSet`s plus a root view; `api/urls.py` registers them on a `NetBoxRouter`; serializers live in `api/serializers_/{providers,circuits,nested}.py` and are re-exported by `api/serializers.py`. [fg:modules:circuits.api.views] [code:netbox/circuits/api/urls.py:5-23] [code:netbox/circuits/api/serializers.py:1-2]

**GraphQL.** `graphql/types.py` (11 strawberry types), `graphql/filters.py` (11 filter types), `graphql/enums.py`, `graphql/filter_mixins.py` (BaseCircuitTypeFilterMixin), and `graphql/schema.py` exposing `CircuitsQuery` with single/list fields per model. [fg:modules:circuits.graphql.types] [fg:modules:circuits.graphql.filters] [code:netbox/circuits/graphql/schema.py:9-42]

**Signals.** `signals.py` registers two receivers on CircuitTermination: `update_circuit` (post_save) writes the termination back onto `Circuit.termination_a/z`; `rebuild_cablepaths` (post_save, post_delete) calls dcim's `rebuild_paths` on the peer termination. [fg:entrypoints:circuits.signals] [code:netbox/circuits/signals.py:8-27]

**Search.** `search.py` registers ten `SearchIndex` classes (all models except the abstract base), with weighted fields. [fg:modules:circuits.search] [code:netbox/circuits/search.py:5-13]

**App config.** `apps.py` imports signals and search in `ready()` and calls `register_models`. [fg:modules:circuits.apps] [code:netbox/circuits/apps.py:8-13]

**Migrations.** Four squashed migrations (0001–0038) then 0043–0052. The recent ones are the history of the current shape: 0044 circuit groups, 0045 distance, 0047 GFK termination, 0048 cached `_site/_region/...` FKs, 0049 natural-sort collation, 0050 virtual circuits, 0051 GFK group member, 0052 wider `_abs_distance`. [fg:modules:circuits.migrations.0047_circuittermination__termination] [fg:modules:circuits.migrations.0050_virtual_circuits] [fg:modules:circuits.migrations.0051_virtualcircuit_group_assignment]

**Tests.** `test_api.py` (12 cases), `test_views.py` (11), `test_filtersets.py` (11), `test_tables.py` (1 regression test on CircuitTerminationTable ordering). [fg:modules:circuits.tests.test_api] [fg:modules:circuits.tests.test_views] [code:netbox/circuits/tests/test_tables.py:7-23]

## Entry points

HTTP: `circuits.urls` (mounted at `circuits/`) and `circuits.api.urls` (mounted at `api/circuits/`). GraphQL: `CircuitsQuery` merged into the root schema. Signals: `circuits.signals`. [fg:entrypoints:circuits.urls] [fg:entrypoints:circuits.api.urls] [code:netbox/netbox/urls.py:26] [code:netbox/netbox/urls.py:45] [fg:imports:netbox.graphql.schema->circuits.graphql.schema]

## What it depends on

Outbound import counts by target: circuits 68 (internal), netbox 37, utilities 34, dcim 22, ipam 13, tenancy 12, core 3, extras 2, users 1. [fg:subsystems:circuits]

**dcim** is the heaviest external dependency and the one with behaviour attached: CircuitTermination inherits `CabledObjectModel`; `CircuitTerminationFilterSet` inherits `CabledObjectFilterSet`; the termination API viewsets mix in `PassThroughPortMixin`; the trace view is dcim's `PathTraceView`; signals call `dcim.signals.rebuild_paths`; the termination serializer inherits `CabledObjectSerializer`; GraphQL types use `CabledObjectMixin`. [fg:imports:circuits.models.circuits->dcim.models] [fg:imports:circuits.filtersets->dcim.filtersets] [fg:imports:circuits.api.views->dcim.api.views] [fg:imports:circuits.views->dcim.views] [fg:imports:circuits.signals->dcim.signals] [fg:imports:circuits.api.serializers_.circuits->dcim.api.serializers_.cables] [fg:imports:circuits.graphql.types->dcim.graphql.mixins]

**String-reference (FK) coupling** to dcim: CircuitTermination has cached FKs `_location`, `_site`, `_region`, `_site_group` (all CASCADE), and VirtualCircuitTermination.interface is a OneToOne to dcim.Interface (CASCADE). Deleting a Site therefore deletes the terminations cached against it. [fg:model_refs:circuits.models.circuits:301] [fg:model_refs:circuits.models.circuits:308] [fg:model_refs:circuits.models.circuits:315] [fg:model_refs:circuits.models.circuits:322] [fg:model_refs:circuits.models.virtual_circuits:138]

**tenancy**: Circuit, CircuitGroup and VirtualCircuit each FK `tenancy.Tenant` (PROTECT); filtersets/forms/tables use TenancyFilterSet, TenancyForm, TenancyColumnsMixin, ContactModelFilterSet. [fg:model_refs:circuits.models.circuits:72] [fg:model_refs:circuits.models.circuits:162] [fg:model_refs:circuits.models.virtual_circuits:64] [fg:imports:circuits.filtersets->tenancy.filtersets]

**ipam**: Provider.asns is an M2M to `ipam.ASN`; ProviderFilterSet, ProviderForm and ProviderListView query ASN directly. [fg:model_refs:circuits.models.providers:32] [fg:imports:circuits.filtersets->ipam.models] [code:netbox/circuits/views.py:22-26]

**contenttypes**: CircuitTermination.termination_type and CircuitGroupAssignment.member_type are FKs to ContentType (PROTECT), backing the two GenericForeignKeys. [fg:model_refs:circuits.models.circuits:248] [fg:model_refs:circuits.models.circuits:183]

**netbox/utilities**: base classes for everything (PrimaryModel, OrganizationalModel, ChangeLoggedModel, NetBoxModelFilterSet, NetBoxTable, NetBoxModelSerializer, generic views, `register_model_view`, `get_model_urls`, ChoiceSet, ColorField). [fg:imports:circuits.models.circuits->netbox.models] [fg:imports:circuits.views->netbox.views] [fg:imports:circuits.urls->utilities.urls] [fg:imports:circuits.models.base->utilities.fields]

## What depends on it

Inbound imports: dcim 12, ipam 5, extras 4, tenancy 2, netbox 1. No other app declares a string FK into circuits (model_refs_in is empty). [fg:subsystems:circuits]

**dcim is a mutual dependency.** `dcim.models.cables` imports CircuitTermination inside functions to follow a cable path A→Z through a circuit and to stop at a provider network; `Cable` validation forbids cabling a termination attached to a ProviderNetwork. `dcim.views` imports Circuit and CircuitTermination to list related circuits on Region/SiteGroup/Site/Location pages, filtering on the cached `_region/_site_group/_site/_location` fields. `dcim.filtersets` imports CircuitTermination, VirtualCircuit and VirtualCircuitTermination for cable and interface filters. `dcim.forms.connections` and `dcim.graphql.gfk_mixins` also import it. [fg:imports:dcim.models.cables->circuits.models] [code:netbox/dcim/models/cables.py:694-705] [code:netbox/dcim/models/cables.py:344-346] [fg:imports:dcim.views->circuits.models] [code:netbox/dcim/views.py:474-482] [fg:imports:dcim.filtersets->circuits.models] [code:netbox/dcim/filtersets.py:1979-1988] [fg:imports:dcim.forms.connections->circuits.models] [fg:imports:dcim.graphql.gfk_mixins->circuits.models]

**ipam** imports Provider for ASN views and filters; **tenancy** and **ipam** GraphQL modules import circuits GraphQL types/filters; **netbox.graphql.schema** merges CircuitsQuery. [fg:imports:ipam.views->circuits.models] [fg:imports:ipam.filtersets->circuits.models] [fg:imports:tenancy.graphql.types->circuits.graphql.types] [fg:imports:ipam.graphql.filters->circuits.graphql.filters] [fg:imports:netbox.graphql.schema->circuits.graphql.schema]

**extras** tests use circuits as their fixture subsystem for custom validation and filterset tests. [fg:imports:extras.tests.test_custom_validation->circuits.models] [fg:imports:extras.tests.test_filtersets->circuits.models]

## Where change concentrates

`views.py` leads with 157 commits from 12 authors (2016–2025-06), followed by the API layer (`api/serializers.py` 89, `api/views.py` 73, `api/urls.py` 29) and `urls.py` (49). Filtersets and their forms are next (45 and 42 commits, 10 authors each, both last touched 2025-03). [fg:churn:circuits.views] [fg:churn:circuits.api.serializers] [fg:churn:circuits.api.views] [fg:churn:circuits.urls] [fg:churn:circuits.filtersets] [fg:churn:circuits.forms.filtersets]

`models/circuits.py` has 41 commits since its 2021 split-out and was last changed 2025-04; `models/virtual_circuits.py` is new (3 commits, 2024-11 to 2025-01). The migrations 0047, 0048 and 0051 were each revised 4–6 times through 2025-06, which is unusual for migrations and reflects the objectchange-migrator hooks appended to them. [fg:churn:circuits.models.circuits] [fg:churn:circuits.models.virtual_circuits] [fg:churn:circuits.migrations.0047_circuittermination__termination] [fg:churn:circuits.migrations.0048_circuitterminations_cached_relations] [fg:churn:circuits.migrations.0051_virtualcircuit_group_assignment] [code:netbox/circuits/migrations/0047_circuittermination__termination.py:55-75]

`api/serializers.py` (89 commits) is now a 2-line re-export; its history predates the 2024-02 move to `serializers_/`, whose modules have 13 and 5 commits. `signals.py` has been static since 2022-05. [fg:churn:circuits.api.serializers] [fg:churn:circuits.api.serializers_.circuits] [fg:churn:circuits.api.serializers_.providers] [fg:churn:circuits.signals]

## Things an engineer should know before touching it

- `Circuit.termination_a/_z` are denormalised caches maintained by a signal, not by the form or serializer; `CircuitSwapTerminations` manipulates them directly with a `'_'` placeholder side to dodge the unique constraint. [code:netbox/circuits/models/circuits.py:96-112] [code:netbox/circuits/signals.py:8-15] [code:netbox/circuits/views.py:385-397]
- `CircuitTermination._region/_site_group/_site/_location/_provider_network` are recomputed on every save from the GFK target; every filter, table column and dcim related-object query reads these, not the GFK. [code:netbox/circuits/models/circuits.py:353-378] [code:netbox/circuits/filtersets.py:280-334] [code:netbox/circuits/tables/circuits.py:127-152]
- The set of allowed termination targets and group members is a closed list in `constants.py`, repeated as ContentType querysets in forms and serializers. [code:netbox/circuits/constants.py:5-12] [code:netbox/circuits/forms/model_forms.py:167-172] [code:netbox/circuits/api/serializers_/circuits.py:126-133]
- Provider-level views cross both circuit families: `ProviderView` adds VirtualCircuits via `provider_network__provider`, and `CircuitGroupAssignmentFilterSet.filter_provider` unions both content types. [code:netbox/circuits/views.py:36-51] [code:netbox/circuits/filtersets.py:453-468]
