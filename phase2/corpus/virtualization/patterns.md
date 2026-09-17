# virtualization — patterns and conventions (NetBox ea4c205)

## P1. One class per model per action, registered by decorator

Every web view is a thin subclass of a `netbox.views.generic` class that sets `queryset`, `filterset`, `filterset_form`, `table` or `form`, and is registered with `@register_model_view(Model, action, ...)`; `urls.py` then only calls `get_model_urls()` per model [code:netbox/virtualization/views.py:29-36] [code:netbox/virtualization/views.py:592-597] [code:netbox/virtualization/urls.py:9-22].

Exception: the two `BulkComponentCreateView` subclasses are not decorated and get explicit `path()` entries in `urls.py` [code:netbox/virtualization/views.py:654-666] [code:netbox/virtualization/urls.py:23-27] [code:netbox/virtualization/urls.py:31-35].

Exception: `ClusterAddDevicesView` and `ClusterRemoveDevicesView` override `get`/`post` entirely and drive `Device.save()` in a transaction rather than using the generic machinery [code:netbox/virtualization/views.py:283-317] [code:netbox/virtualization/views.py:326-361].

## P2. Child-object tabs use `ObjectChildrenView` + `ViewTab` with a permission and a badge

Cluster → VMs, Cluster → Devices, VM → Interfaces, VM → Disks all follow the same shape: `child_model`, `table`, `filterset`, `filterset_form`, a `ViewTab(label, badge, permission, weight)`, and `get_children()` that applies `restrict(request.user, 'view')` [code:netbox/virtualization/views.py:200-215] [code:netbox/virtualization/views.py:382-405] [code:netbox/virtualization/views.py:408-428].

Badges read counter-cache fields where they exist (`interface_count`, `virtual_disk_count`) and fall back to `.count()` where they do not (cluster VMs and devices) [code:netbox/virtualization/views.py:394-399] [code:netbox/virtualization/views.py:207-212] [code:netbox/virtualization/views.py:233-238].

Exception: `ClusterDevicesView` uses `dcim`'s table/filterset/form and declares a custom `actions` dict including `bulk_remove_devices` [code:netbox/virtualization/views.py:218-232].

## P3. Related-object counts are annotated on the queryset, not computed per row

List, bulk-edit and bulk-delete views annotate `cluster_count`, `device_count`, `vm_count` with `count_related()`; tables render them as `LinkedCountColumn` pointing at the filtered list view; the API annotates `allocated_vcpus/memory/disk` with `Sum()` and uses `RelatedObjectCountField` for counts [code:netbox/virtualization/views.py:163-172] [code:netbox/virtualization/tables/clusters.py:84-93] [code:netbox/virtualization/api/views.py:36-43] [code:netbox/virtualization/api/serializers_/clusters.py:71-73].

## P4. VM components share an abstract `ComponentModel`

`VMInterface` and `VirtualDisk` inherit `ComponentModel`, which gives the `virtual_machine` CASCADE FK, a unique `(virtual_machine, name)` constraint, `to_objectchange()` that attaches the parent VM as `related_object`, and `parent_object` [code:netbox/virtualization/models/virtualmachines.py:266-305] [code:netbox/virtualization/models/virtualmachines.py:308-308] [code:netbox/virtualization/models/virtualmachines.py:417-417].

The same split is mirrored in forms (`VMComponentForm` disables re-parenting on edit), GraphQL (`ComponentType`, `VMComponentFilterMixin`) and filtersets (`virtual_machine`/`virtual_machine_id` filters on both) [code:netbox/virtualization/forms/model_forms.py:293-305] [code:netbox/virtualization/graphql/types.py:38-43] [code:netbox/virtualization/graphql/filter_mixins.py:19-26] [code:netbox/virtualization/filtersets.py:298-308].

Exception: `VMInterface` overrides `related_name` to `interfaces` (so `vm.interfaces`, not `vm.vminterfaces`), while `VirtualDisk` keeps the default `vm.virtualdisks` [code:netbox/virtualization/models/virtualmachines.py:319-323] [code:netbox/virtualization/models/virtualmachines.py:206-206].

## P5. Interface behaviour is inherited from `dcim`, then VM-specific validation is layered on

`VMInterface` gets `enabled`, `mtu`, `mode`, `parent`, `bridge`, VLAN fields and `primary_mac_address` from `dcim.BaseInterface`; its own `clean()` only adds "same virtual machine" checks for parent/bridge and a site check for the untagged VLAN [code:netbox/dcim/models/device_components.py:512-515] [code:netbox/virtualization/models/virtualmachines.py:368-410].

The same layering appears in forms (`InterfaceCommonForm` + `VMComponentForm`), filtersets (`CommonInterfaceFilterSet`), tables (`BaseInterfaceTable`), and GraphQL (`InterfaceBaseFilterMixin`) [code:netbox/virtualization/forms/model_forms.py:308-308] [code:netbox/virtualization/filtersets.py:235-235] [code:netbox/virtualization/tables/virtualmachines.py:103-103] [code:netbox/virtualization/graphql/filters.py:133-134].

## P6. Cross-VM VLAN checks live in the serializer, not the model

Tagged-VLAN site agreement for `VMInterface` is validated in `VMInterfaceSerializer.validate()` (with an explicit note about being reached through custom-field assignment), while the untagged-VLAN check is in the model `clean()` [code:netbox/virtualization/api/serializers_/virtualmachines.py:114-142] [code:netbox/virtualization/models/virtualmachines.py:403-410] [code:netbox/virtualization/tests/test_api.py:362-392].

## P7. Dynamic form fields are chained with `query_params` on `$field` references

Model forms, bulk-edit forms and filter forms narrow choices through `DynamicModelChoiceField(query_params={...: '$other'})`: cluster by site, device by cluster+site, parent/bridge by `$virtual_machine`, VLANs by `$vlan_group` and `available_on_virtualmachine` [code:netbox/virtualization/forms/model_forms.py:182-200] [code:netbox/virtualization/forms/model_forms.py:316-354] [code:netbox/virtualization/forms/filtersets.py:214-221].

Exception: bulk-edit forms that cannot know the VM up front add the parameter at `__init__` via `widget.add_query_param()`, and disable parent/bridge entirely when editing across VMs [code:netbox/virtualization/forms/bulk_edit.py:264-275] [code:netbox/virtualization/forms/bulk_edit.py:301-304].

## P8. Roles offered for VMs are restricted with `vm_role=True`

Every place a VM role is chosen filters `DeviceRole` on `vm_role`, either as a queryset filter or a `query_params` hint: model form, bulk edit, import, filter form [code:netbox/virtualization/forms/model_forms.py:201-208] [code:netbox/virtualization/forms/bulk_edit.py:126-135] [code:netbox/virtualization/forms/bulk_import.py:111-119] [code:netbox/virtualization/forms/filtersets.py:156-164] [code:netbox/dcim/models/devices.py:384-384].

## P9. Filtersets expose paired `<name>_id` / `<name>` filters and a `search()` over text fields

For each relation there is an ID filter and a slug/name filter, and each filterset defines `search()` combining `name`, `description` and (for primary models) `comments` [code:netbox/virtualization/filtersets.py:43-62] [code:netbox/virtualization/filtersets.py:115-124] [code:netbox/virtualization/filtersets.py:72-79] [code:netbox/virtualization/filtersets.py:216-226].

Cluster-derived filters on child models traverse the FK (`virtual_machine__cluster`, `cluster__group__slug`) instead of duplicating data [code:netbox/virtualization/filtersets.py:93-103] [code:netbox/virtualization/filtersets.py:236-246].

## P10. Serializers: nested related serializers, explicit `fields`, explicit `brief_fields`

All serializers subclass `NetBoxModelSerializer`, declare related objects as `XSerializer(nested=True, ...)`, and list `fields` and `brief_fields` explicitly; tests assert `brief_fields` per model [code:netbox/virtualization/api/serializers_/virtualmachines.py:32-57] [code:netbox/virtualization/api/serializers_/clusters.py:47-82] [code:netbox/virtualization/tests/test_api.py:164-166].

Exception: self-referential fields (`parent`, `bridge`) use the old-style `NestedVMInterfaceSerializer` from `nested.py` rather than `nested=True` [code:netbox/virtualization/api/serializers_/virtualmachines.py:82-83] [code:netbox/virtualization/api/serializers_/nested.py:17-22].

Exception: `VirtualMachineViewSet` overrides `get_serializer_class()` to swap between the plain and `WithConfigContext` serializers based on `brief` and `?exclude=config_context` [code:netbox/virtualization/api/views.py:54-68] [code:netbox/virtualization/tests/test_api.py:239-258].

## P11. GraphQL types are `strawberry_django.type(..., fields='__all__', filters=..., pagination=True)` with lazy cross-app annotations

Every type declares related objects as `Annotated["OtherType", strawberry.lazy('app.graphql.types')]`, and cross-app imports are under `TYPE_CHECKING` to avoid cycles [code:netbox/virtualization/graphql/types.py:13-26] [code:netbox/virtualization/graphql/types.py:91-113] [code:netbox/virtualization/graphql/filters.py:19-30].

Exception: `ClusterType` excludes the scope/cached fields and exposes `scope` as a union resolver [code:netbox/virtualization/graphql/types.py:46-66].

Observation: `VirtualMachineType` declares `interface_count: BigInt` twice [code:netbox/virtualization/graphql/types.py:98-100].

## P12. Module-level `__all__` and star re-exports

Every non-trivial module declares `__all__`, and package `__init__` files re-export with `from .x import *`, so consumers import from `virtualization.models`, `virtualization.forms`, `virtualization.tables` [code:netbox/virtualization/models/virtualmachines.py:24-28] [code:netbox/virtualization/forms/__init__.py:1-6] [code:netbox/virtualization/api/serializers.py:1-2] [fg:imports:dcim.views->virtualization.forms].

## P13. Data migrations pair a `RunPython` forward with `noop` reverse and an `objectchange_migrators` hook

Migrations that reshape data (0044 scope, 0045 cached FKs, 0048 MAC addresses) each ship a forward function, `reverse_code=migrations.RunPython.noop`, and a module-level `objectchange_migrators` dict to rewrite historical change-log payloads [code:netbox/virtualization/migrations/0044_cluster_scope.py:45-63] [code:netbox/virtualization/migrations/0045_clusters_cached_relations.py:73-100] [code:netbox/virtualization/migrations/0048_populate_mac_addresses.py:49-94].

## P14. Ordering by natural sort: DB collation for most names, `NaturalOrderingField` for interfaces

`Cluster.name`, `VirtualMachine.name` and `ComponentModel.name` use `db_collation="natural_sort"` (migration 0047 dropped the old `_name` columns on VM and VirtualDisk), while `VMInterface` re-declares `name` without collation and keeps a `_name = NaturalOrderingField(naturalize_interface)` ordered through `CollateAsChar` [code:netbox/virtualization/models/virtualmachines.py:70-74] [code:netbox/virtualization/migrations/0047_natural_ordering.py:19-41] [code:netbox/virtualization/models/virtualmachines.py:309-318] [code:netbox/virtualization/models/virtualmachines.py:363-366].

## P15. Tests use the shared `ViewTestCases`/`APIViewTestCases`/`ChangeLoggedFilterSetTests` harnesses

View tests pick the harness by model kind (`OrganizationalObjectViewTestCase`, `PrimaryObjectViewTestCase`, `DeviceComponentViewTestCase`); filterset tests mix in `ChangeLoggedFilterSetTests`; API tests set `brief_fields` and add targeted regression tests [code:netbox/virtualization/tests/test_views.py:13-13] [code:netbox/virtualization/tests/test_views.py:95-95] [code:netbox/virtualization/tests/test_views.py:327-327] [code:netbox/virtualization/tests/test_filtersets.py:14-14] [code:netbox/virtualization/tests/test_api.py:394-394].

## Observation: table default column not in `fields`

`ClusterTable.Meta.default_columns` lists `'site'` but the `fields` tuple has `scope`/`scope_type` and no `site` column [code:netbox/virtualization/tables/clusters.py:101-107].
