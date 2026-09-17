# dcim — retro-ADRs (decisions the code embodies)

## ADR-1: Cable paths are materialised, not computed on demand

**Context.** Tracing a connection may cross front/rear port fan-outs, circuits, provider networks and wireless links; list views and filters need "is this port connected?" cheaply. [code:netbox/dcim/models/cables.py:404-437]

**Decision.** A `CablePath` row stores the whole trace as a JSON list of hops, each hop a list of `"<ct_id>:<pk>"` node strings, plus a flattened `_nodes` ArrayField (custom `PathField`) with a registered `PathContains` lookup so any object can be looked up with `_nodes__contains=obj`. Origin endpoints hold a direct `_path` FK back to the row. Paths are (re)built only by signal receivers on Cable / CableTermination / FrontPort changes, and by the `trace_paths` command for backfill. [code:netbox/dcim/models/cables.py:439-476] [code:netbox/dcim/fields.py:82-91] [code:netbox/dcim/lookups.py:6-10] [code:netbox/dcim/models/device_components.py:222-227] [code:netbox/dcim/signals.py:74-118] [code:netbox/dcim/management/commands/trace_paths.py:70-90]

**Consequences.** `connected` filtering is a join on `_path__is_active`; API `/trace` and the UI trace page read the stored path rather than walking cables. The cost is that correctness depends on every mutation reaching a receiver — hence `Cable.save()` sends a dedicated `trace_paths` Signal after terminations are persisted, imports (`raw=True`) skip retracing, and an `UnsupportedCablePath` raised during tracing is converted to `AbortRequest` so the save is rejected rather than leaving a stale path. The path model is marked `_netbox_private` and has no CRUD UI. [code:netbox/dcim/filtersets.py:1640-1649] [code:netbox/dcim/api/views.py:37-74] [code:netbox/dcim/models/cables.py:239-242] [code:netbox/dcim/signals.py:75-82] [code:netbox/dcim/models/cables.py:457]

## ADR-2: Terminations live in a separate generic table, but the endpoint keeps a cached back-pointer

**Context.** A cable end may attach to several objects of one type (e.g. multiple front ports), and to objects in other apps (CircuitTermination). [code:netbox/dcim/models/cables.py:248-250] [code:netbox/dcim/constants.py:104-118]

**Decision.** `CableTermination` (cable, cable_end, GenericFK) is the source of truth, with a uniqueness constraint per terminated object. Every cable-able model also carries `cable` and `cable_end` columns (CabledObjectModel); `CableTermination.save()` / `delete()` write those columns onto the endpoint, and `Cable` exposes `a_terminations` / `b_terminations` as Python-level lists that its `save()` diffs against existing rows. [code:netbox/dcim/models/cables.py:252-271] [code:netbox/dcim/models/cables.py:301-308] [code:netbox/dcim/models/device_components.py:131-156] [code:netbox/dcim/models/cables.py:348-371] [code:netbox/dcim/models/cables.py:218-238]

**Consequences.** Endpoint queries (`cable__isnull`, `link_peers`) stay simple joins, but three places must agree: the termination table, the endpoint columns and the CablePath. A `post_delete` receiver on CableTermination exists to null the endpoint columns when deletion bypasses `delete()`. Cable creation must supply both ends up front, and the cable edit view has to construct a form class per termination-type pair. [code:netbox/dcim/filtersets.py:1620-1637] [code:netbox/dcim/signals.py:120-132] [code:netbox/dcim/models/cables.py:165-166] [code:netbox/dcim/views.py:3552-3572]

## ADR-3: Termination compatibility is a static matrix, not a model relationship

**Decision.** Which endpoint types may be joined is a dictionary constant (`COMPATIBLE_TERMINATION_TYPES`) keyed by model name, checked in `Cable.clean()`; which ContentTypes may terminate at all is a `Q` limiter (`CABLE_TERMINATION_MODELS`). Interface types that cannot take a cable are another constant list (`NONCONNECTABLE_IFACE_TYPES`) checked in `CableTermination.clean()`. [code:netbox/dcim/constants.py:120-130] [code:netbox/dcim/models/cables.py:175-182] [code:netbox/dcim/constants.py:38-63] [code:netbox/dcim/models/cables.py:336-342]

**Consequences.** Adding a terminable model or interface type is a constants edit plus a views-level mapping (`CABLE_TERMINATION_TYPES`) and the `get_cable_form` factory; `constants.py` therefore churns like feature code (129 commits). [code:netbox/dcim/views.py:38-48] [code:netbox/dcim/forms/connections.py:11-60] [fg:churn:dcim.constants]

## ADR-4: Components are copied from templates at creation time, never linked

**Context.** A DeviceType describes hardware; a Device is one instance whose ports may later diverge (renamed, deleted, modules inserted). [code:netbox/dcim/models/devices.py:440-450]

**Decision.** `Device.save()` on insert walks each template relation and `bulk_create`s concrete components via `template.instantiate(device=…)`; `Module.save()` does the same from ModuleType templates with `{module}` substituted from the module-bay position chain, and can instead *adopt* existing same-named components. No FK from component to template is kept. [code:netbox/dcim/models/devices.py:942-956] [code:netbox/dcim/models/device_component_templates.py:157-179] [code:netbox/dcim/models/modules.py:287-323] [code:netbox/dcim/models/devices.py:887-905]

**Consequences.** Editing a template never touches existing devices; the only cross-check is DeviceType.clean refusing height changes that would not fit racked instances. Bulk creation bypasses `save()`, so the code re-emits `post_save` manually and cannot bulk-create MPTT models (ModuleBay, InventoryItem). Components and templates are also forbidden from changing parent after creation. [code:netbox/dcim/models/devices.py:296-314] [code:netbox/dcim/models/devices.py:906-915] [code:netbox/dcim/models/modules.py:330-346] [code:netbox/dcim/models/device_components.py:94-101]

## ADR-5: Generic "scope" and cross-app terminations are made filterable by cached FK columns

**Context.** Objects such as prefixes, VLAN groups, clusters and circuit terminations may be scoped to a Region, SiteGroup, Site or Location through one GenericFK; cable terminations may belong to a device, a rack or a site. Filtering a GenericFK by hierarchy is not expressible in the ORM. [code:netbox/dcim/models/mixins.py:37-57]

**Decision.** `CachedScopeMixin` adds `_region/_site_group/_site/_location` FKs and fills all four from the scope on every save; `CableTermination` does the same with `_device/_rack/_location/_site`, and `DCIMConfig.ready()` registers those columns with `netbox.denormalized` so parent changes propagate. Filtersets (`ScopedFilterSet`) and site-change signals target the cache columns. [code:netbox/dcim/models/mixins.py:97-120] [code:netbox/dcim/models/cables.py:373-396] [code:netbox/dcim/apps.py:19-31] [code:netbox/dcim/base_filtersets.py:17-67] [code:netbox/dcim/signals.py:24-30]

**Consequences.** ipam, virtualization, wireless and circuits reuse the mixin, filterset and form trio, making dcim the owner of a cross-app convention. Any new ancestor level means touching the mixin, the constants tuple, the form mixins and the filterset together. [fg:imports:ipam.filtersets->dcim.base_filtersets] [fg:model_refs:circuits.models.circuits:301] [fg:imports:wireless.forms.model_forms->dcim.forms.mixins] [code:netbox/dcim/constants.py:133-135]

## ADR-6: Site/location consistency is enforced after the fact by signal cascade

**Decision.** Rather than validating that every child agrees with its parent on each write, `post_save` receivers on Location and Rack push the new site/location into descendants, racks, devices, power panels and CableTermination caches using `QuerySet.update()`; `Device.save()` likewise pushes site/rack/location into child devices in its bays. `Device.clean()` still validates its own rack/location/site triple. [code:netbox/dcim/signals.py:18-40] [code:netbox/dcim/models/devices.py:958-964] [code:netbox/dcim/models/devices.py:712-728]

**Consequences.** Reparenting is one write from the user's perspective, but the `update()` path skips model `save()` and therefore change logging and other signals — contradicting the receiver's own docstring, which claims per-object recursion was chosen precisely to create change records. [code:netbox/dcim/signals.py:20-30]

## ADR-7: RackType attributes are copied onto Rack, and re-synced when the type changes

**Decision.** `Rack` and `RackType` share `RackBase`; `Rack.save()` calls `copy_racktype_attrs()` to overwrite its physical fields from `rack_type`, and `RackType.save()` iterates its racks, snapshots and re-saves each. [code:netbox/dcim/models/racks.py:39] [code:netbox/dcim/models/racks.py:414-431] [code:netbox/dcim/models/racks.py:202-207]

**Consequences.** Elevation rendering and filtering read plain Rack columns without joins; a RackType edit is O(racks) writes with change-log entries for each. [code:netbox/dcim/models/racks.py:562-604] [code:netbox/dcim/models/racks.py:202-207]

## ADR-8: Module attributes are schema-driven via ModuleTypeProfile

**Decision.** Instead of fixed columns per module kind, `ModuleTypeProfile.schema` is a user-editable JSON Schema validated on save, and `ModuleType.clean()` validates `attribute_data` against the assigned profile (clearing it when there is no schema). Six starter profiles ship as JSON fixtures loaded by data migration 0206. [code:netbox/dcim/models/modules.py:27-63] [code:netbox/dcim/models/modules.py:143-150] [code:netbox/dcim/migrations/0206_load_module_type_profiles.py:7-32]

**Consequences.** Filtering on module attributes goes through an `AttributeFiltersMixin` rather than concrete filters, and profile deletion is guarded by a PROTECT FK from ModuleType. [code:netbox/dcim/filtersets.py:694] [fg:model_refs:dcim.models.modules:72]

## ADR-9: The Device API serialises config context by default, with an opt-out serializer

**Decision.** `DeviceViewSet.get_serializer_class()` returns `DeviceWithConfigContextSerializer` unless the request is `brief` or lists `config_context` in `exclude`, in which case the plain `DeviceSerializer` is used; the viewset also uses `StripCountAnnotationsPaginator`. [code:netbox/dcim/api/views.py:373-399] [code:netbox/dcim/api/serializers_/devices.py:106-107]

**Consequences.** Rendered config context is computed per device on every default list call, which is why the opt-out exists and why the queryset prefetches `parent_bay`. [code:netbox/dcim/api/views.py:379-381]
