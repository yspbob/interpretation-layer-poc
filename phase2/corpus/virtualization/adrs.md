# virtualization — retro-ADRs (NetBox ea4c205)

## ADR-V1. Cluster location is a generic "scope", not a Site FK

**Context.** Before migration 0044 `Cluster` had a plain `site` FK; clusters that span a location, or that are organised by region, could not express that [code:netbox/virtualization/migrations/0044_cluster_scope.py:6-18].

**Decision.** `Cluster` inherits `dcim.CachedScopeMixin`: a `scope_type`/`scope_id` GenericForeignKey to Region, SiteGroup, Site or Location, plus cached `_region`, `_site_group`, `_site`, `_location` FKs that the mixin recomputes in `save()` via `cache_related_objects()`. Migration 0044 added the GFK and copied `site_id` into it; 0045 added the cached FKs, back-filled them, dropped `site`, and re-created the name-uniqueness constraint against `_site` [code:netbox/virtualization/models/clusters.py:47-47] [code:netbox/dcim/models/mixins.py:37-57] [code:netbox/dcim/models/mixins.py:97-119] [code:netbox/virtualization/migrations/0044_cluster_scope.py:27-45] [code:netbox/virtualization/migrations/0045_clusters_cached_relations.py:5-19] [code:netbox/virtualization/migrations/0045_clusters_cached_relations.py:72-88].

**Consequences.** Everything that used to read `cluster.site` now reads `cluster._site`: `VirtualMachine.clean()`/`save()`, `Device.clean()`, the signal that pushes site to VMs, and the bulk-edit form's site inference. Cluster `clean()` must resolve the scope model by `apps.get_model` to decide whether to check devices by site or by location. The uniqueness constraint `(_site, name)` only applies when the scope is (or resolves to) a site. Filter forms expose `region_id`/`site_group_id`/`site_id`/`location_id` through `ScopedFilterSet` rather than local filters [code:netbox/virtualization/models/virtualmachines.py:185-190] [code:netbox/dcim/models/devices.py:859-869] [code:netbox/virtualization/signals.py:19-25] [code:netbox/virtualization/forms/bulk_edit.py:289-290] [code:netbox/virtualization/models/clusters.py:122-129] [code:netbox/virtualization/models/clusters.py:105-108] [code:netbox/virtualization/forms/filtersets.py:47-47].

**Evidence.** Two change-log migrators rewrite historical `site` values into `scope_type`/`scope_id` and then strip `site`, showing the rename was intended to be invisible to change-log consumers [code:netbox/virtualization/migrations/0044_cluster_scope.py:49-63] [code:netbox/virtualization/migrations/0045_clusters_cached_relations.py:92-100] [fg:model_refs:virtualization.migrations.0044_cluster_scope:12].

## ADR-V2. A VM's site is derived from its cluster and kept in sync by a signal

**Context.** A VM must be placeable without a cluster (site-only) and a clustered VM must not contradict its cluster's site [code:netbox/virtualization/tests/test_models.py:64-80].

**Decision.** `VirtualMachine.site` is a real nullable FK. `clean()` requires site or cluster, rejects a site that differs from `cluster._site`; `save()` fills `site` from `cluster._site` when unset; and a `post_save` receiver on `Cluster` bulk-updates every VM's `site` to the cluster's `_site` whenever the cluster is saved with a site [code:netbox/virtualization/models/virtualmachines.py:178-190] [code:netbox/virtualization/models/virtualmachines.py:238-244] [code:netbox/virtualization/signals.py:19-25].

**Consequences.** `site` is denormalised and can be filtered/joined directly (`site__region`, `site__group`), at the cost of two write paths that must agree. The signal uses `.update()`, so VM `save()`/change-logging does not run for the pushed-down site. A cluster whose scope is a location still yields a site because `_site` is cached from the location [code:netbox/virtualization/filtersets.py:135-160] [code:netbox/virtualization/signals.py:24-25] [code:netbox/virtualization/models/clusters.py:127-129].

**Evidence.** The model tests assert both the mismatch rejection and the auto-fill [code:netbox/virtualization/tests/test_models.py:73-80].

## ADR-V3. `VirtualMachine.disk` is a stored aggregate of `VirtualDisk.size`, and disks are MB

**Context.** Migration 0038 introduced `VirtualDisk` alongside the pre-existing scalar `VirtualMachine.disk`; both had to coexist for users who never model individual disks [code:netbox/virtualization/migrations/0038_virtualdisk.py:18-26].

**Decision.** Keep `disk` as a nullable column. A `post_save`/`post_delete` receiver on `VirtualDisk` rewrites the VM's `disk` with `Sum('size')` via `.update()`; `VirtualMachine.clean()` refuses a `disk` value that disagrees with the disk total once disks exist; the edit form disables the field in that state. Migration 0040 multiplied all existing values by `DISK_BASE_UNIT` and recomputed aggregates, fixing the unit as MB [code:netbox/virtualization/signals.py:8-16] [code:netbox/virtualization/models/virtualmachines.py:204-215] [code:netbox/virtualization/forms/model_forms.py:246-251] [code:netbox/virtualization/migrations/0040_convert_disk_size.py:6-19].

**Consequences.** Bulk edit and CSV import can still set `disk` directly; validation catches mismatches only through `full_clean()`. Cluster-level `allocated_disk` in the API is a plain `Sum` over VMs, so it counts scalar and aggregated disks alike. Tables humanise the MB value on render [code:netbox/virtualization/forms/bulk_edit.py:154-157] [code:netbox/virtualization/api/views.py:37-41] [code:netbox/virtualization/tables/virtualmachines.py:95-96].

**Evidence.** `test_disk_size` checks create/delete recomputation and the rejection of a manual overwrite [code:netbox/virtualization/tests/test_models.py:98-121].

## ADR-V4. VM name uniqueness is case-insensitive per cluster, and tenant-scoped

**Context.** Names may legitimately repeat across tenants sharing a cluster, but not within one tenant or when no tenant is set [code:netbox/virtualization/tests/test_models.py:16-45].

**Decision.** Two `UniqueConstraint`s on `Lower('name')`: `(name, cluster, tenant)` and a conditional `(name, cluster)` where `tenant IS NULL`, with a custom violation message. `Meta.ordering` is `('name', 'pk')` because names are non-unique globally [code:netbox/virtualization/models/virtualmachines.py:155-168].

**Consequences.** Uniqueness is enforced only when `cluster` is set; site-only VMs with duplicate names are allowed by the constraints. The `name` filter uses `iexact` to match this semantics [code:netbox/virtualization/filtersets.py:171-173].

**Evidence.** `test_vm_name_case_sensitivity` and the API `test_unique_name_per_cluster_constraint` [code:netbox/virtualization/tests/test_models.py:82-96] [code:netbox/virtualization/tests/test_api.py:260-260].

## ADR-V5. Child interfaces protect their parents (`RESTRICT`), and bulk delete orders around it

**Context.** Deleting a parent interface while children still reference it would either cascade silently or fail [code:netbox/virtualization/migrations/0037_protect_child_interfaces.py:1-1].

**Decision.** Migration 0037 changed `VMInterface.parent` to `on_delete=RESTRICT`. Both the UI `VMInterfaceBulkDeleteView` and the API `get_bulk_destroy_queryset()` order by `('virtual_machine', 'parent', CollateAsChar('_name'))` so children are deleted before parents within one bulk operation [code:netbox/virtualization/migrations/0037_protect_child_interfaces.py:13-23] [code:netbox/virtualization/views.py:580-583] [code:netbox/virtualization/api/views.py:80-82].

**Consequences.** Single-object delete of a parent with children fails; the ordering trick is duplicated in two places and must be kept identical [code:netbox/virtualization/tests/test_views.py:419-446].

## ADR-V6. Interface MAC addresses are first-class `dcim.MACAddress` objects; the old scalar is a compatibility shim

**Context.** `VMInterface.mac_address` was a scalar column until NetBox 4.2 [code:netbox/virtualization/api/serializers_/virtualmachines.py:99-100].

**Decision.** Migration 0048 adds `primary_mac_address` (OneToOne to `dcim.MACAddress`, inherited via `BaseInterface`), creates one `MACAddress` per existing value assigned back to the interface, then drops the column. `VMInterface` keeps a `mac_addresses` GenericRelation; the serializer exposes read-only `mac_address` for older clients plus writable `primary_mac_address` and read-only `mac_addresses`; filtering by MAC traverses `mac_addresses__mac_address` [code:netbox/virtualization/migrations/0048_populate_mac_addresses.py:7-53] [code:netbox/virtualization/models/virtualmachines.py:356-361] [code:netbox/virtualization/api/serializers_/virtualmachines.py:99-102] [code:netbox/virtualization/filtersets.py:196-199] [code:netbox/virtualization/filtersets.py:268-282].

**Consequences.** A change-log migrator creates/deletes `MACAddress` rows when replaying old changes, and is explicitly coupled to its `dcim` peer migration [code:netbox/virtualization/migrations/0048_populate_mac_addresses.py:57-94] [fg:model_refs:virtualization.migrations.0048_populate_mac_addresses:59].

## ADR-V7. Reuse `dcim` abstractions rather than fork them

**Context.** VM interfaces need the same 802.1Q, MTU, parent/bridge and MAC semantics as device interfaces, and clusters need the same scope semantics as other located objects [code:netbox/dcim/models/device_components.py:512-515].

**Decision.** `VMInterface` extends `dcim.BaseInterface`; `Cluster` extends `dcim.CachedScopeMixin`; forms, filtersets, tables and GraphQL filters extend the `dcim` common/scoped mixins; `ClusterDevicesView` reuses `DeviceTable`/`DeviceFilterSet`/`DeviceFilterForm` outright; `dcim` in turn reuses the VM table/filterset for its device tab [fg:imports:virtualization.models.virtualmachines->dcim.models] [fg:imports:virtualization.models.clusters->dcim.models.mixins] [fg:imports:virtualization.forms.model_forms->dcim.forms.common] [fg:imports:virtualization.filtersets->dcim.filtersets] [code:netbox/virtualization/views.py:218-224] [code:netbox/dcim/views.py:2353-2358].

**Consequences.** `dcim` is 43 of the outbound import edges and 16 of the inbound ones; a change to `BaseInterface` or the scope mixins lands here automatically, and the form/filterset churn tracks `dcim`/`ipam` field additions (Q-in-Q, VLAN translation) rather than local features [fg:subsystems:virtualization] [code:netbox/virtualization/migrations/0042_vminterface_vlan_translation_policy.py:1-1] [code:netbox/virtualization/migrations/0043_qinq_svlan.py:12-14] [fg:churn:virtualization.forms.filtersets].

## ADR-V8. Config context is opt-out on the VM API, not opt-in

**Context.** Rendered config context is expensive and only sometimes wanted [code:netbox/virtualization/api/views.py:54-63].

**Decision.** The default serializer is `VirtualMachineWithConfigContextSerializer`; the plain serializer is used only for `brief` or `?exclude=config_context`. The queryset uses `ConfigContextQuerySetMixin`, and the model manager is `ConfigContextModelQuerySet` [code:netbox/virtualization/api/views.py:64-68] [code:netbox/virtualization/models/virtualmachines.py:146-146] [code:netbox/virtualization/api/serializers_/virtualmachines.py:60-73].

**Evidence.** Tests assert config context is present by default in list views and absent when excluded [code:netbox/virtualization/tests/test_api.py:239-258].

## ADR-V9. Split the API serializers by model family behind a re-export shim

**Context.** `api/serializers.py` absorbed 90 commits from 2017 to 2024 as a single file [fg:churn:virtualization.api.serializers].

**Decision.** From 2024 the content lives in `serializers_/clusters.py` and `serializers_/virtualmachines.py`, with `serializers.py` reduced to two star-imports so `from . import serializers` in `api/views.py` keeps working; other apps import the submodules directly [code:netbox/virtualization/api/serializers.py:1-2] [code:netbox/virtualization/api/views.py:9-9] [fg:imports:dcim.api.serializers_.devices->virtualization.api.serializers_.clusters] [fg:churn:virtualization.api.serializers_.virtualmachines].
