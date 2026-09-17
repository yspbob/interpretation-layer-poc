# virtualization — map (NetBox ea4c205)

## What it is

The `virtualization` app models six things: `ClusterType`, `ClusterGroup`, `Cluster`, `VirtualMachine`, `VMInterface` and `VirtualDisk`. It is a small app (42 modules, ~6.1k lines of code, 5 test modules) whose models are shaped almost entirely by `dcim`, `ipam` and the `netbox` core base classes rather than by anything local [fg:subsystems:virtualization] [code:netbox/virtualization/models/clusters.py:13-17] [code:netbox/virtualization/models/virtualmachines.py:24-28].

## Modules by role

**Models.** `models/clusters.py` holds the three cluster models; `Cluster` mixes in `dcim`'s `CachedScopeMixin` (a GenericForeignKey scope to Region/SiteGroup/Site/Location plus cached `_site`, `_location`, `_region`, `_site_group` FKs) and enforces host-device/scope agreement in `clean()` [code:netbox/virtualization/models/clusters.py:47-50] [code:netbox/virtualization/models/clusters.py:119-146] [fg:model_refs:virtualization.models.clusters:125]. `models/virtualmachines.py` holds `VirtualMachine` (site/cluster/device/tenant/platform/role FKs, two primary-IP OneToOnes, counter-cache fields) and the abstract `ComponentModel` from which `VMInterface` and `VirtualDisk` inherit; `VMInterface` also inherits `dcim.BaseInterface` for the 802.1Q, parent/bridge and MAC fields [code:netbox/virtualization/models/virtualmachines.py:31-31] [code:netbox/virtualization/models/virtualmachines.py:266-274] [code:netbox/virtualization/models/virtualmachines.py:308-308] [fg:symbols:virtualization.models.virtualmachines:ComponentModel].

**Choices.** Two `ChoiceSet`s, `ClusterStatusChoices` and `VirtualMachineStatusChoices`, each with a color per status; the GraphQL enums are derived from them [code:netbox/virtualization/choices.py:10-25] [code:netbox/virtualization/graphql/enums.py:10-11].

**Views and URLs.** `views.py` (680 lines, 56 classes) is one class per model per action, registered with `@register_model_view`; `urls.py` builds routes through `get_model_urls()` plus two hand-written routes for bulk component creation [code:netbox/virtualization/views.py:29-36] [code:netbox/virtualization/urls.py:9-35] [fg:modules:virtualization.views] [fg:entrypoints:virtualization.urls]. The only view logic that is not declarative is the device add/remove pair on `Cluster`, the `VMInterfaceView` context assembly, and the list-view annotations [code:netbox/virtualization/views.py:277-317] [code:netbox/virtualization/views.py:320-361] [code:netbox/virtualization/views.py:500-539].

**Forms.** Split by purpose into `model_forms`, `filtersets`, `object_create`, `bulk_create`, `bulk_edit`, `bulk_import`, all star-exported from `forms/__init__.py` [code:netbox/virtualization/forms/__init__.py:1-6] [fg:modules:virtualization.forms.model_forms] [fg:modules:virtualization.forms.bulk_edit].

**Tables.** `tables/clusters.py` and `tables/virtualmachines.py`; `VMInterfaceTable` extends `dcim`'s `BaseInterfaceTable`, and `template_code.py` holds the raw Django template string for the per-row "add IP / MAC / L2VPN / FHRP / tunnel" buttons [code:netbox/virtualization/tables/virtualmachines.py:103-103] [code:netbox/virtualization/tables/template_code.py:1-32] [fg:imports:virtualization.tables.virtualmachines->dcim.tables.devices].

**Filtersets.** One `django_filters` filterset per model, composed from `netbox`, `tenancy`, `dcim`, `extras` and `ipam` mixins [code:netbox/virtualization/filtersets.py:42-42] [code:netbox/virtualization/filtersets.py:82-88] [code:netbox/virtualization/filtersets.py:235-235].

**REST API.** `api/serializers.py` is a two-line re-export of `serializers_/clusters.py` and `serializers_/virtualmachines.py`; `serializers_/nested.py` keeps two `WritableNestedSerializer`s for parent/bridge self-references; `api/views.py` has six viewsets on a `NetBoxRouter` [code:netbox/virtualization/api/serializers.py:1-2] [code:netbox/virtualization/api/serializers_/nested.py:10-22] [code:netbox/virtualization/api/urls.py:5-16] [fg:entrypoints:virtualization.api.views].

**GraphQL.** `graphql/types.py` (strawberry types), `graphql/filters.py`, `graphql/filter_mixins.py` (`VMComponentFilterMixin`), `graphql/enums.py`, `graphql/schema.py` (`VirtualizationQuery`, merged into the root schema by `netbox.graphql.schema`) [code:netbox/virtualization/graphql/schema.py:9-27] [fg:imports:netbox.graphql.schema->virtualization.graphql.schema] [fg:symbols:virtualization.graphql.filter_mixins:VMComponentFilterMixin].

**Search.** Six `SearchIndex` classes registered with `@register_search` [code:netbox/virtualization/search.py:5-13] [fg:modules:virtualization.search].

**Signals and app config.** `signals.py` has two receivers: recompute `VirtualMachine.disk` when a `VirtualDisk` changes, and push a cluster's `_site` down to its VMs on `Cluster` save. `apps.py` imports `search` and `signals` in `ready()`, registers all models, and connects counter caches for `VirtualMachine` [code:netbox/virtualization/signals.py:8-25] [code:netbox/virtualization/apps.py:7-17] [fg:entrypoints:virtualization.signals].

**Migrations.** Two squashed migrations (0001–0022, 0023–0036) and twelve later ones; the ones that carry design decisions are 0037 (parent FK → RESTRICT), 0038 (VirtualDisk + counter), 0040 (disk unit conversion), 0044/0045/0046 (site FK → scope GFK + cached FKs), 0047 (natural-sort collation) and 0048 (MAC address extraction) [fg:modules:virtualization.migrations.0044_cluster_scope] [fg:modules:virtualization.migrations.0048_populate_mac_addresses] [code:netbox/virtualization/migrations/0037_protect_child_interfaces.py:13-23].

**Tests.** `test_api`, `test_filtersets`, `test_views`, `test_models`; the model tests cover name uniqueness per cluster/tenant, site/cluster agreement, case-insensitive names and disk aggregation [code:netbox/virtualization/tests/test_models.py:16-47] [code:netbox/virtualization/tests/test_models.py:82-121] [fg:modules:virtualization.tests.test_filtersets] [fg:modules:virtualization.tests.test_views].

## Entry points

Web URLs are mounted under the `virtualization` namespace at `cluster-types/`, `cluster-groups/`, `clusters/`, `virtual-machines/`, `interfaces/`, `virtual-disks/`; REST under `virtualization-api` at the same six prefixes; GraphQL through `VirtualizationQuery`; and the two signal receivers fire on model events [code:netbox/virtualization/urls.py:6-22] [code:netbox/virtualization/api/urls.py:9-19] [fg:entrypoints:virtualization.urls] [fg:entrypoints:virtualization.api.urls] [fg:entrypoints:virtualization.signals].

## What it depends on

Outbound import edges by target: `virtualization` 62 (internal), `dcim` 43, `utilities` 43, `netbox` 29, `ipam` 20, `extras` 17, `tenancy` 13, `vpn` 3, `core` 1 [fg:subsystems:virtualization] [fg:imports:virtualization.models.clusters->dcim.models.mixins].

The heaviest structural dependency is `dcim`: the models inherit `CachedScopeMixin`, `RenderConfigMixin` and `BaseInterface` from it, the forms inherit `ScopedForm`/`ScopedImportForm`/`ScopedBulkEditForm` and `InterfaceCommonForm`, the filtersets inherit `ScopedFilterSet` and `CommonInterfaceFilterSet`, and `ClusterDevicesView` reuses `DeviceTable`, `DeviceFilterSet` and `DeviceFilterForm` wholesale [fg:imports:virtualization.models.virtualmachines->dcim.models] [fg:imports:virtualization.forms.model_forms->dcim.forms.common] [fg:imports:virtualization.filtersets->dcim.base_filtersets] [code:netbox/virtualization/views.py:218-224].

String-reference (FK/GenericRelation) targets out of the app: `dcim.Site`, `dcim.Device`, `dcim.Platform`, `dcim.DeviceRole`, `dcim.MACAddress`, `tenancy.Tenant`, `ipam.IPAddress` (primary IPs and interface addresses), `ipam.VRF`, `ipam.Service`, `ipam.VLANGroup`, `ipam.FHRPGroupAssignment`, `vpn.TunnelTermination`, `vpn.L2VPNTermination` [fg:model_refs:virtualization.models.virtualmachines:35] [fg:model_refs:virtualization.models.virtualmachines:49] [fg:model_refs:virtualization.models.virtualmachines:88] [fg:model_refs:virtualization.models.virtualmachines:344] [fg:model_refs:virtualization.models.virtualmachines:356] [fg:model_refs:virtualization.models.clusters:84].

`extras` supplies `ConfigContextModel`, `ConfigContextModelQuerySet` and the config-context/render-config views and API mixins that `VirtualMachine` uses [fg:imports:virtualization.models.virtualmachines->extras.models] [fg:imports:virtualization.views->extras.views] [fg:imports:virtualization.api.views->extras.api.mixins] [code:netbox/virtualization/api/views.py:50-50].

## What depends on it

Inbound import edges: `dcim` 16, `ipam` 14, `extras` 11, `vpn` 6, `tenancy` 2, `netbox` 1, `utilities` 1 [fg:subsystems:virtualization] [fg:imports:dcim.views->virtualization.models].

- `dcim.Device.cluster` is a `SET_NULL` FK to `virtualization.Cluster`, and `Device.clean()` checks the device's site/location against the cluster's cached `_site`/`_location`; `dcim.views.DeviceVirtualMachinesView` reuses the VM table, filterset and filter form [fg:model_refs:dcim.models.devices:569] [code:netbox/dcim/models/devices.py:859-869] [code:netbox/dcim/views.py:2353-2368] [fg:imports:dcim.views->virtualization.tables].
- `extras.ConfigContext` has M2M fields to `ClusterType`, `ClusterGroup` and `Cluster`, so config-context matching depends on the cluster hierarchy [fg:model_refs:extras.models.configs:85] [fg:model_refs:extras.models.configs:90] [fg:model_refs:extras.models.configs:95].
- `ipam.signals.clear_primary_ip` clears `VirtualMachine.primary_ip4/6` when an `IPAddress` is deleted; `ipam.filtersets` exposes `available_on_virtualmachine` for VLAN selection [fg:imports:ipam.signals->virtualization.models] [code:netbox/ipam/signals.py:50-63] [code:netbox/ipam/filtersets.py:1018-1018].
- `vpn`, `ipam` and `dcim` GraphQL types/filters import the virtualization GraphQL types for lazy cross-references [fg:imports:vpn.graphql.types->virtualization.graphql.types] [fg:imports:ipam.graphql.types->virtualization.graphql.types] [fg:imports:dcim.graphql.types->virtualization.graphql.types].
- `utilities.testing.utils` imports the models, so the shared test helpers know about VMs [fg:imports:utilities.testing.utils->virtualization.models].

## Where change concentrates

`views.py` dominates churn (185 commits, 16 authors, 2017–2025), followed by the old monolithic `api/serializers.py` (90 commits, now a re-export shim) and `api/views.py` (73); the newer split serializer modules have 12 and 7 commits since 2024 [fg:churn:virtualization.views] [fg:churn:virtualization.api.serializers] [fg:churn:virtualization.api.views] [fg:churn:virtualization.api.serializers_.virtualmachines] [fg:churn:virtualization.api.serializers_.clusters].

Among non-view modules, the forms (`forms/filtersets` 38, `forms/bulk_edit` 36, `forms/model_forms` 28, `forms/bulk_import` 24) and `filtersets.py` (36) change most, tracking each new field that `dcim`/`ipam` add to interfaces; the VM model file has 30 commits since its 2022 split from a single `models.py` [fg:churn:virtualization.forms.filtersets] [fg:churn:virtualization.forms.bulk_edit] [fg:churn:virtualization.filtersets] [fg:churn:virtualization.models.virtualmachines].

Tests move with the code: `test_api` 62, `test_views` 54, `test_filtersets` 30 [fg:churn:virtualization.tests.test_api] [fg:churn:virtualization.tests.test_views] [fg:churn:virtualization.tests.test_filtersets].

## Things to know before editing

- `Cluster` has no `site` field any more; `_site` is the cached FK derived from `scope`, and both `VirtualMachine.clean()`/`save()` and `Device.clean()` read `cluster._site` directly [code:netbox/virtualization/models/virtualmachines.py:185-190] [code:netbox/virtualization/models/virtualmachines.py:240-242] [code:netbox/dcim/models/devices.py:859-863] [code:netbox/virtualization/migrations/0045_clusters_cached_relations.py:78-82].
- `ClusterImportForm` still declares a `site` CSV field that is absent from its `Meta.fields`, even though `Cluster` has no `site` column; the `ScopedImportForm` mixin contributes only `scope_type`, and `scope_id` is listed as a plain field [code:netbox/virtualization/forms/bulk_import.py:59-65] [code:netbox/virtualization/forms/bulk_import.py:74-81] [code:netbox/dcim/forms/mixins.py:104-109].
- `VirtualMachine.disk` is both a user-editable field and a signal-maintained aggregate of `VirtualDisk.size`; the form disables it once disks exist and `clean()` rejects mismatches [code:netbox/virtualization/models/virtualmachines.py:204-215] [code:netbox/virtualization/forms/model_forms.py:246-251] [code:netbox/virtualization/signals.py:8-16].
- `VMInterfaceSerializer.mac_address` is a read-only compatibility field after MACs moved to `dcim.MACAddress` in migration 0048 [code:netbox/virtualization/api/serializers_/virtualmachines.py:99-102] [code:netbox/virtualization/migrations/0048_populate_mac_addresses.py:38-53].
- Bulk-delete of `VMInterface` orders by `('virtual_machine', 'parent', CollateAsChar('_name'))` in both the UI and API because `parent` is `RESTRICT` [code:netbox/virtualization/views.py:580-583] [code:netbox/virtualization/api/views.py:80-82] [code:netbox/virtualization/migrations/0037_protect_child_interfaces.py:13-23].
