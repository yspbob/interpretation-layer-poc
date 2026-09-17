# ipam — patterns and conventions (NetBox @ ea4c205)

## 1. One view family per model, wired by decorator

Every model gets list, detail, add+edit, delete, bulk_import, bulk_edit and bulk_delete classes on `netbox.views.generic`, each tagged `@register_model_view(Model, name, path=..., detail=...)`; `urls.py` contributes only two `get_model_urls()` includes per model. Instances: VRF, Prefix. [code:netbox/ipam/views.py:31-72] [code:netbox/ipam/views.py:75-92] [code:netbox/ipam/views.py:502-508] [code:netbox/ipam/views.py:653-682] [code:netbox/ipam/urls.py:15-16]

Exceptions: FHRPGroupAssignment has only add/edit/delete and its `get_absolute_url` redirects to the interface; IPAddress adds `assign`, `bulk_add` and `related_ips`, and `IPAddressAssignView` carries a "standardize or remove" TODO. [code:netbox/ipam/views.py:1258-1281] [code:netbox/ipam/models/fhrp.py:122-126] [code:netbox/ipam/views.py:866-868] [code:netbox/ipam/views.py:913-919]

## 2. Child tabs delegate to model helpers and restrict by user

Child views subclass `ObjectChildrenView`, declare a `ViewTab` whose badge counts via a model helper, and implement `get_children()` as `parent.get_child_*()` followed by `.restrict(request.user, 'view')`. Instances: PrefixPrefixesView, PrefixIPRangesView, VLANGroupVLANsView, IPAddressRelatedIPsView. [code:netbox/ipam/views.py:560-578] [code:netbox/ipam/views.py:596-614] [code:netbox/ipam/views.py:1016-1034] [code:netbox/ipam/views.py:943-958]

## 3. Query helpers live on the model

Containment, availability, duplicates and utilization are methods on the model and are consumed by views, API and forms alike. Instances: `Prefix.get_child_prefixes/get_child_ranges/get_child_ips/get_available_ips/get_utilization`, `Aggregate.get_utilization`, `IPRange.get_available_ips`, `VLANGroup.get_available_vids`, `ASNRange.get_available_asns`. [code:netbox/ipam/models/ip.py:376-405] [code:netbox/ipam/models/ip.py:407-437] [code:netbox/ipam/models/ip.py:171-179] [code:netbox/ipam/models/ip.py:670-680] [code:netbox/ipam/models/vlans.py:139-159] [code:netbox/ipam/models/asns.py:80-88]

## 4. Fake "available" rows share tables with real rows

When a child tab is neither searched nor ordered, `prep_table_data()` replaces the queryset with a list mixing real objects and unsaved placeholders: `Prefix(prefix=p, status=None)` for gaps, `AvailableIPSpace` dataclasses for IP gaps, plain dicts for VLAN gaps. Templates and columns branch on `record.pk`. [code:netbox/ipam/views.py:580-585] [code:netbox/ipam/views.py:641-644] [code:netbox/ipam/views.py:1036-1039] [code:netbox/ipam/utils.py:49-54] [code:netbox/ipam/utils.py:19-33] [code:netbox/ipam/utils.py:157-162] [code:netbox/ipam/tables/template_code.py:5-11] [code:netbox/ipam/tables/ip.py:147-154]

## 5. Network containment goes through custom PostgreSQL lookups

`IPNetworkField` maps to `cidr`, `IPAddressField` to `inet`; both return `netaddr.IPNetwork` and register `net_contains`, `net_contained`, `net_contained_or_equal`, `net_host`, `net_host_contained`, `net_in`, `family`, `net_mask_length`, plus text lookups that wrap the column in `TEXT()`. Callers pass `str(prefix)`. Instances: `GetAvailablePrefixesMixin`, `Aggregate.clean`, `Prefix.get_child_ips`, `PrefixFilterSet.search_within`, `IPAddressFilterSet.search_by_parent`. [code:netbox/ipam/fields.py:56-109] [code:netbox/ipam/lookups.py:4-10] [code:netbox/ipam/lookups.py:143-154] [code:netbox/ipam/models/ip.py:39-46] [code:netbox/ipam/models/ip.py:130-131] [code:netbox/ipam/models/ip.py:402-405] [code:netbox/ipam/filtersets.py:415-423] [code:netbox/ipam/filtersets.py:685-695]

Ordering of IP addresses is forced to `INET(HOST(address))` by the manager, backed by a functional index on `Cast(Host('address'))`. [code:netbox/ipam/managers.py:7-17] [code:netbox/ipam/models/ip.py:792-797]

## 6. Filterset parsing conventions

`search()` builds a `Q` over description plus prefix/address text; `parent`/`within`/`contains` method filters parse with `netaddr` and return `queryset.none()` on failure; `present_in_vrf` joins through route targets; `filter_address` uses `net_in` after `parse_inet_addresses`. [code:netbox/ipam/filtersets.py:393-404] [code:netbox/ipam/filtersets.py:435-447] [code:netbox/ipam/filtersets.py:450-456] [code:netbox/ipam/filtersets.py:697-727] [code:netbox/ipam/filtersets.py:730-736]

Exception: `PrimaryIPFilterSet` is a bare `django_filters.FilterSet` not attached to any ipam model; it exists to be mixed into dcim and virtualization filtersets. [code:netbox/ipam/filtersets.py:1250-1275] [code:netbox/dcim/filtersets.py:1315] [fg:imports:virtualization.filtersets->ipam.filtersets]

## 7. "Available object" API views are a template method with an advisory lock

`AvailableObjectsView` fixes the GET/POST flow (`get_parent`, `get_available_objects`, `get_extra_context`, `check_sufficient_available`, `prep_object_data`) and wraps POST in `advisory_lock(ADVISORY_LOCK_KEYS[key])`, answering 409 when short; subclasses for ASN, Prefix, IPAddress (prefix and range parents) and VLAN fill in the hooks and are routed by explicit paths rather than the router. [code:netbox/ipam/api/views.py:202-251] [code:netbox/ipam/api/views.py:253-304] [code:netbox/ipam/api/views.py:307-332] [code:netbox/ipam/api/views.py:347-385] [code:netbox/ipam/api/views.py:444-453] [code:netbox/ipam/api/views.py:456-480] [code:netbox/ipam/api/urls.py:31-57]

Read-side serializers for available objects are plain `serializers.Serializer` subclasses whose `to_representation` reads `parent`/`vrf`/`group` from context. [code:netbox/ipam/api/serializers_/ip.py:112-129] [code:netbox/ipam/api/serializers_/ip.py:193-211] [code:netbox/ipam/api/serializers_/vlans.py:86-101]

Exceptions: `AvailablePrefixesView` overrides `check_sufficient_available` because requests are sized; `PrefixViewSet.get_serializer_class` swaps in `PrefixLengthSerializer` for that action; `CreateAvailableVLANSerializer.validate` deliberately skips model validation because no VID exists yet. [code:netbox/ipam/api/views.py:359-364] [code:netbox/ipam/api/views.py:91-94] [code:netbox/ipam/api/serializers_/vlans.py:104-118]

## 8. Generic foreign keys bounded by `Q` constants

Each GFK has a companion `Q` constant in `constants.py` restricting content types; serializers apply it to `ContentTypeField`, forms use an HTMX `scope_type`/`parent_object_type` select whose partner `DynamicModelChoiceField` is retargeted in `__init__` and assigned in `clean()`, and `Meta.indexes` carries a composite (type, id) index. Instances: `IPAddress.assigned_object` with `IPADDRESS_ASSIGNMENT_MODELS`; `Service.parent` with `SERVICE_ASSIGNMENT_MODELS`; `VLANGroup.scope` with `VLANGROUP_SCOPE_TYPES`; `FHRPGroupAssignment.interface`. [code:netbox/ipam/constants.py:31-35] [code:netbox/ipam/constants.py:86-90] [code:netbox/ipam/constants.py:77-79] [code:netbox/ipam/api/serializers_/ip.py:166-170] [code:netbox/ipam/forms/model_forms.py:760-800] [code:netbox/ipam/forms/model_forms.py:808-834] [code:netbox/ipam/forms/model_forms.py:608-668] [code:netbox/ipam/models/services.py:92-95] [code:netbox/ipam/models/fhrp.py:105-109]

GFK targets are serialised through `SerializerMethodField` + `get_serializer_for_model(...)(nested=True)` and exposed in GraphQL as `strawberry.union` fields. [code:netbox/ipam/api/serializers_/ip.py:184-190] [code:netbox/ipam/api/serializers_/vlans.py:54-60] [code:netbox/ipam/graphql/types.py:155-161] [code:netbox/ipam/graphql/types.py:191-198]

Exceptions: `IPAddressForm` offers three separate selector fields (`interface`, `vminterface`, `fhrpgroup`) and enforces "exactly one" in `clean()` instead of a type dropdown; `Prefix.scope` reuses dcim's `CachedScopeMixin`/`ScopedForm` rather than an ipam-local implementation. [code:netbox/ipam/forms/model_forms.py:392-416] [code:netbox/ipam/models/ip.py:201] [code:netbox/ipam/forms/model_forms.py:204]

## 9. VRF-qualified uniqueness is a `clean()` policy, not a constraint

`vrf=None` is the global table; duplicates are checked in `clean()` via `get_duplicates()` only when `ENFORCE_GLOBAL_UNIQUE` (global) or `vrf.enforce_unique` applies, and ordering places null VRFs first with a "may be non-unique" comment. Instances: Prefix, IPAddress, IPRange ordering. [code:netbox/ipam/models/ip.py:302-311] [code:netbox/ipam/models/ip.py:875-887] [code:netbox/ipam/models/ip.py:276] [code:netbox/ipam/models/ip.py:541] [code:netbox/ipam/models/vrfs.py:39-43]

Exception: IPAddress roles in `IPADDRESS_ROLES_NONUNIQUE` are exempt; the detail view likewise hides anycast duplicates. [code:netbox/ipam/constants.py:40-48] [code:netbox/ipam/models/ip.py:877-880] [code:netbox/ipam/views.py:816-818]

## 10. Cached counters are written, not computed

Derived values are stored on the row and refreshed in `save()` or signals: `IPRange.size`, `VLANGroup._total_vlan_ids`, `Prefix._depth/_children` (signals and `rebuild_prefixes`), Prefix `_site/_region/_site_group/_location` (`cache_related_objects()` in `save()` plus `denormalized.register` in `apps.ready`). [code:netbox/ipam/models/ip.py:609-614] [code:netbox/ipam/models/vlans.py:132-137] [code:netbox/ipam/models/ip.py:259-267] [code:netbox/ipam/signals.py:9-49] [code:netbox/ipam/models/ip.py:313-323] [code:netbox/ipam/apps.py:18-25]

## 11. Cross-app parent updates use `snapshot()` then `save()`

Whenever ipam mutates a Device/VirtualMachine field (primary IP, OOB IP) it calls `snapshot()` first so the change log captures the prior state. Instances: `clear_primary_ip`, `clear_oob_ip`, `IPAddressForm.save`. [code:netbox/ipam/signals.py:53-65] [code:netbox/ipam/signals.py:68-76] [code:netbox/ipam/forms/model_forms.py:435-466]

## 12. Facade modules and star imports

`models/__init__`, `api/serializers.py`, `forms/__init__`, `tables/__init__` are pure re-export facades and leaf modules declare `__all__`; consumers write `from ipam.models import *`. [code:netbox/ipam/models/__init__.py:1-7] [code:netbox/ipam/api/serializers.py:1-7] [code:netbox/ipam/tables/__init__.py:1-6] [code:netbox/ipam/models/ip.py:23-30] [code:netbox/ipam/api/views.py:19]

Consequence worth knowing: `constants.py` imports `Q` and has no `__all__`, so `Q` reaches `models/ip.py` (used in `IPRange.clean`) and `views.py` (used in `PrefixView`) only via `from ipam.constants import *`; neither module imports `Q` itself. [code:netbox/ipam/constants.py:1] [code:netbox/ipam/models/ip.py:1-21] [code:netbox/ipam/models/ip.py:574-594] [code:netbox/ipam/views.py:1-24] [code:netbox/ipam/views.py:524-527]

## 13. Serializer shape

Model serializers extend `NetBoxModelSerializer`, nest FKs with `nested=True`, expose `family` as a read-only `ChoiceField`, use `IPNetworkField`/`IPAddressField` serializer fields, and declare `brief_fields`. Instances: Aggregate, Prefix, IPRange, IPAddress. [code:netbox/ipam/api/serializers_/ip.py:31-43] [code:netbox/ipam/api/serializers_/ip.py:46-74] [code:netbox/ipam/api/serializers_/ip.py:136-152] [code:netbox/ipam/api/serializers_/ip.py:159-182]

Exception: `nested.py` keeps two `WritableNestedSerializer`s for self-referential fields (`nat_inside`, `qinq_svlan`). [code:netbox/ipam/api/serializers_/nested.py:13-26] [code:netbox/ipam/api/serializers_/ip.py:172-173] [code:netbox/ipam/api/serializers_/vlans.py:70]

## 14. GraphQL type declaration

Types use `@strawberry_django.type(model, fields='__all__', filters=..., pagination=True)` and reference peers through `Annotated[..., strawberry.lazy(...)]`; `PrefixType` is the one that `exclude`s fields (the raw scope and cached scope columns). [code:netbox/ipam/graphql/types.py:71-80] [code:netbox/ipam/graphql/types.py:164-175] [code:netbox/ipam/graphql/types.py:178-189]
