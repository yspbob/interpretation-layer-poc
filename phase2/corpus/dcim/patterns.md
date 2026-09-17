# dcim — established patterns and conventions

## Module organisation

**Package façades via star re-export.** Split packages expose a flat namespace: `models/__init__.py` star-imports eight submodules, `api/serializers.py` is a 14-line shim over `api/serializers_/*`, and each submodule declares `__all__` to bound what leaks. Callers then write `from dcim.models import *` or `from .models import *`. [code:netbox/dcim/models/__init__.py:1-8] [code:netbox/dcim/api/serializers.py:1-13] [code:netbox/dcim/models/cables.py:22-26] [code:netbox/dcim/views.py:36]

**Choices and constants are star-imported into models.** `models/cables.py`, `models/device_components.py` and others open with `from dcim.choices import *` and `from dcim.constants import *`. Exception to watch: `constants.py` itself imports `Q` at module level, and `cables.py` uses `Q` in `CablePath.from_origin` without importing it — it arrives only through the constants star import. [code:netbox/dcim/models/cables.py:10-13] [code:netbox/dcim/models/device_components.py:11-12] [code:netbox/dcim/constants.py:1] [code:netbox/dcim/models/cables.py:607-616]

## Model layer

**Behaviour is composed from small abstract bases, with MRO chosen per class.** ComponentModel (device FK, name/label/description, unique-per-device) is extended by ModularComponentModel (module FK, inventory_items GenericRelation); CabledObjectModel adds `cable`/`cable_end`/`mark_connected`; PathEndpoint adds `_path`. Concrete classes stack them: `ConsolePort(ModularComponentModel, CabledObjectModel, PathEndpoint, TrackingModelMixin)`, `Interface(ModularComponentModel, BaseInterface, CabledObjectModel, PathEndpoint, TrackingModelMixin)`, `FrontPort(ModularComponentModel, CabledObjectModel, TrackingModelMixin)` (no PathEndpoint), and `PowerFeed(PrimaryModel, PathEndpoint, CabledObjectModel)` outside the component family. [code:netbox/dcim/models/device_components.py:42-76] [code:netbox/dcim/models/device_components.py:126-159] [code:netbox/dcim/models/device_components.py:277] [code:netbox/dcim/models/device_components.py:641] [code:netbox/dcim/models/device_components.py:1028] [code:netbox/dcim/models/power.py:72]

**Every template class names its concrete twin and instantiates it.** Templates set `component_model = <Component>` and implement `instantiate(**kwargs)` returning an unsaved instance with `resolve_name(module)` / `resolve_label(module)` applied; the base `ComponentTemplateModel.instantiate` raises NotImplementedError. `Device._instantiate_components` reads `queryset.model.component_model` to know what to bulk-create. [code:netbox/dcim/models/device_component_templates.py:77-81] [code:netbox/dcim/models/device_component_templates.py:206-218] [code:netbox/dcim/models/device_component_templates.py:169-191] [code:netbox/dcim/models/devices.py:887-905]

**Underscore-prefixed denormalised columns exist purely for filtering and ordering, and are recomputed in `save()`.** CableTermination caches `_device/_rack/_location/_site`; CachedScopeMixin caches `_region/_site_group/_site/_location` from a GenericFK scope; PathEndpoint holds `_path`; CablePath holds `_nodes` (flattened path); Cable holds `_abs_length`; RackType/Rack hold `_abs_max_weight`; Interface holds `_name` (NaturalOrderingField). Each is populated by a `cache_related_objects()` or inline computation before `super().save()`. [code:netbox/dcim/models/cables.py:273-297] [code:netbox/dcim/models/cables.py:348-396] [code:netbox/dcim/models/mixins.py:59-82] [code:netbox/dcim/models/mixins.py:97-120] [code:netbox/dcim/models/cables.py:466-476] [code:netbox/dcim/models/cables.py:84-90] [code:netbox/dcim/models/racks.py:189-195] [code:netbox/dcim/models/device_components.py:646-648]

**Filtersets target the cache columns, not the GenericFK.** `ScopedFilterSet` filters `region_id` on `_region`, `site` on `_site__slug`, etc.; the same convention appears in `DeviceComponentFilterSet` (which instead traverses `device__site__region` because components have a real FK). [code:netbox/dcim/base_filtersets.py:17-67] [code:netbox/dcim/filtersets.py:1491-1538]

**Original values are captured in `__init__` so `clean()` can detect forbidden changes.** `ComponentModel._original_device`, `ComponentTemplateModel._original_device_type`, `Cable._orig_status`, and `DeviceType._original_u_height` are all read from `self.__dict__` at construction; components and templates may not be moved between parents (InventoryItem is the one explicit exemption). [code:netbox/dcim/models/device_components.py:78-101] [code:netbox/dcim/models/device_component_templates.py:83-100] [code:netbox/dcim/models/cables.py:99-108] [code:netbox/dcim/models/devices.py:285-310]

**Dimensioned values are stored twice: user unit plus a normalised base unit.** Cable length → `_abs_length` in metres via `to_meters`; rack max weight → `_abs_max_weight` in grams via `to_grams`; `Device.total_weight` sums module and device-type `_abs_weight`. A value without a unit is rejected in `clean()`, and a unit without a value is cleared in `save()`. [code:netbox/dcim/models/cables.py:161-163] [code:netbox/dcim/models/cables.py:203-211] [code:netbox/dcim/models/racks.py:178-201] [code:netbox/dcim/models/devices.py:1041-1051]

**`bulk_create` is used for component instantiation, with `post_save` re-sent by hand; MPTT models are the exception and are saved one by one.** Both `Device.save()` (module bays and inventory items with `bulk_create=False`) and `Module.save()` (`if component_model is not ModuleBay`) follow this split, and both apply CustomField defaults before creating. [code:netbox/dcim/models/devices.py:897-922] [code:netbox/dcim/models/devices.py:942-956] [code:netbox/dcim/models/modules.py:325-346]

**Change-log attribution is redirected to the parent object.** `to_objectchange()` sets `related_object` to `self.device` (components), `self.device_type` or `self.module_type` (templates), and `self.termination` (CableTermination). [code:netbox/dcim/models/device_components.py:89-92] [code:netbox/dcim/models/device_component_templates.py:136-142] [code:netbox/dcim/models/cables.py:398-401]

**Mutating helpers are flagged `alters_data = True`.** Applied to `cache_related_objects` on CableTermination and CachedScopeMixin and to `CablePath.retrace`, so templates cannot call them. [code:netbox/dcim/models/cables.py:396] [code:netbox/dcim/models/mixins.py:120] [code:netbox/dcim/models/cables.py:755]

**Allowed ContentTypes are expressed as `Q` limiters in `constants.py`.** `CABLE_TERMINATION_MODELS`, `MODULAR_COMPONENT_MODELS`, `MODULAR_COMPONENT_TEMPLATE_MODELS`, `MACADDRESS_ASSIGNMENT_MODELS`, and the tuple `LOCATION_SCOPE_TYPES` (used by the Scoped form mixins). [code:netbox/dcim/constants.py:72-94] [code:netbox/dcim/constants.py:104-118] [code:netbox/dcim/constants.py:133-145] [code:netbox/dcim/forms/mixins.py:22-28]

**`clone_fields` is declared on most concrete models** to drive "clone" pre-population (Cable, ConsolePort, Interface, ModuleBay, Rack, Location, Module). [code:netbox/dcim/models/cables.py:92] [code:netbox/dcim/models/device_components.py:297] [code:netbox/dcim/models/modules.py:240] [code:netbox/dcim/models/sites.py:303]

## Signals

**Parent-assignment consistency is enforced by `post_save` receivers that cascade with `QuerySet.update()`.** `handle_location_site_change` and `handle_rack_site_change` push site/location down to descendants, racks, devices, power panels and cached CableTermination columns. Exception: the first receiver's docstring says it "intentionally recurse[s] through each child object instead of calling update()" to create change records, but the body calls `.update()` throughout — the comment and the code disagree. [code:netbox/dcim/signals.py:18-40]

**Cable path maintenance is signal-driven, keyed on a custom `trace_paths` Signal rather than `post_save`.** `Cable.save()` sends `trace_paths`; the receiver decides between `create_cablepath` (PathEndpoint origins) and `rebuild_paths` (pass-through origins); deletion of Cable, CableTermination and creation of FrontPort each retrace affected CablePaths found with `_nodes__contains`. [code:netbox/dcim/models/cables.py:30] [code:netbox/dcim/models/cables.py:239-242] [code:netbox/dcim/signals.py:74-118] [code:netbox/dcim/signals.py:120-143]

## Views, URLs, forms

**One decorator + one URL helper per model.** Every model's list/detail/add/edit/delete/bulk views are `@register_model_view(Model, action, path=…, detail=…)` decorated, and `urls.py` includes `get_model_urls('dcim', <model>, detail=False)` and `get_model_urls('dcim', <model>)` pairs; the rack elevation list is the only hand-wired URL. [code:netbox/dcim/views.py:215-230] [code:netbox/dcim/views.py:271-306] [code:netbox/dcim/views.py:320-335] [code:netbox/dcim/views.py:397-433] [code:netbox/dcim/urls.py:9-30]

**Child-object tabs subclass a per-parent `ObjectChildrenView` base.** `DeviceComponentsView`, `DeviceTypeComponentsView` and `ModuleTypeComponentsView` define `get_children` once; concrete tabs (e.g. `DeviceInterfacesView`) supply `child_model`, `table`, `filterset`, `filterset_form`, `template_name` and a `ViewTab`. [code:netbox/dcim/views.py:51-92] [code:netbox/dcim/views.py:2219-2233]

**Pattern-expanded creation uses `ComponentCreateForm` + `generic.ComponentCreateView`.** Create forms mix `ComponentCreateForm` (ExpandableNameField `name`/`label`, `replication_fields`) into the model form and exclude the plain fields; there is one such form and view per component and per template. [code:netbox/dcim/forms/object_create.py:37-75] [code:netbox/dcim/forms/object_create.py:81-108] [code:netbox/dcim/views.py:1581-1621] [code:netbox/dcim/views.py:2488-2525]

**Cable forms are generated per termination-type pair.** `get_cable_form(a_type, b_type)` builds a ModelForm via a custom metaclass; `CableEditView.alter_object` resolves the types from GET/POST or the existing terminations and swaps `self.form`, documented in-code as a "hack". [code:netbox/dcim/forms/connections.py:11-60] [code:netbox/dcim/views.py:3547-3572]

**Scope selection is a reusable form trio.** `ScopedForm`, `ScopedBulkEditForm`, `ScopedImportForm` (HTMX-driven `scope_type` → `scope` field) are imported by ipam, virtualization and wireless. [code:netbox/dcim/forms/mixins.py:22-72] [code:netbox/dcim/forms/mixins.py:74-109] [fg:imports:ipam.forms.model_forms->dcim.forms.mixins] [fg:imports:virtualization.forms.model_forms->dcim.forms.mixins]

## Filtersets

**Filtersets are assembled from plain `django_filters.FilterSet` mixins.** `DeviceComponentFilterSet`, `ModularDeviceComponentFilterSet`, `CabledObjectFilterSet`, `PathEndpointFilterSet` carry no `Meta`; concrete filtersets inherit several plus `NetBoxModelFilterSet` (e.g. ConsolePortFilterSet lists four bases). [code:netbox/dcim/filtersets.py:1486-1490] [code:netbox/dcim/filtersets.py:1619-1650] [code:netbox/dcim/filtersets.py:1652-1665]

**Related-object filters come in `<name>_id` / `<name>` pairs** (pk vs slug/name/model), with tree models using `TreeNodeMultipleChoiceFilter` and `lookup_expr='in'`. [code:netbox/dcim/filtersets.py:1491-1503] [code:netbox/dcim/filtersets.py:1560-1570] [code:netbox/dcim/base_filtersets.py:18-30]

## API, GraphQL, tables

**Cabling actions are mixins on viewsets.** `PathEndpointMixin` (`/trace`, SVG when `?render=svg`) is applied to the six endpoint viewsets; `PassThroughPortMixin` (`/paths`) to FrontPort/RearPort. [code:netbox/dcim/api/views.py:37-88] [code:netbox/dcim/api/views.py:418-460] [code:netbox/dcim/api/views.py:477-492] [code:netbox/dcim/api/views.py:575-580]

**Table cell markup lives in `template_code.py` as uppercase string constants** consumed through `columns.TemplateColumn`, star-imported into table modules. [code:netbox/dcim/tables/template_code.py:1-40] [code:netbox/dcim/tables/devices.py:8] [code:netbox/dcim/tables/devices.py:344-370]

**GraphQL exposes `<model>` and `<model>_list` per type**, all in `DCIMQuery`, with types star-imported from `types.py`. [code:netbox/dcim/graphql/schema.py:6-40]

## Tests and migrations

**Each model has a mirrored test class in `test_api`, `test_views` and `test_filtersets`** (e.g. RegionTest / RegionTestCase in all three), while cable-path behaviour is one numbered-topology class in `test_cablepaths`. [fg:symbols:dcim.tests.test_api:RegionTest] [fg:symbols:dcim.tests.test_views:RegionTestCase] [fg:symbols:dcim.tests.test_filtersets:RegionTestCase] [code:netbox/dcim/tests/test_cablepaths.py:11-20]

**Migrations are squashed in ranges with `replaces`**, and data migrations use `apps.get_model` plus RunPython (0206 loads JSON fixtures for ModuleTypeProfile from `initial_data/`). [code:netbox/dcim/migrations/0003_squashed_0130.py:16-18] [code:netbox/dcim/migrations/0206_load_module_type_profiles.py:7-44] [fg:model_refs:dcim.migrations.0206_load_module_type_profiles:13]
