# wireless — patterns and conventions (T0 ea4c205)

## P1. One class per model per layer, three models per module

Every layer module defines exactly three classes, one per concrete model, in the fixed order group / LAN / link: filtersets, each of the four form modules, GraphQL filters and types, search indexes, and API viewsets. `views.py` scales this to seven views per model. [fg:symbols:wireless.filtersets:WirelessLANGroupFilterSet] [fg:symbols:wireless.forms.bulk_edit:WirelessLinkBulkEditForm] [fg:symbols:wireless.graphql.types:WirelessLinkType] [code:netbox/wireless/search.py:5-31] [code:netbox/wireless/api/views.py:17-38]

Exception: `tables/` splits by model file instead (`wirelesslan.py` holds group + LAN + an interface table; `wirelesslink.py` holds the link), and `api/serializers_/` splits the same way with an extra `nested.py`. [code:netbox/wireless/tables/wirelesslan.py:9-13] [code:netbox/wireless/api/serializers_/nested.py:7-10]

## P2. Behaviour comes from framework mixins, not local code

Concrete models compose abstract bases rather than implementing features: `WirelessLAN` is `WirelessAuthenticationBase + CachedScopeMixin + PrimaryModel`; `WirelessLink` is `WirelessAuthenticationBase + DistanceMixin + PrimaryModel`; `WirelessLANGroup` is `NestedGroupModel`. The same composition is repeated at every layer: `ScopedFilterSet`/`TenancyFilterSet` on the LAN filterset, `ScopedForm`/`TenancyForm` on the LAN form, `ScopedBulkEditForm`, `ScopedImportForm`, `DistanceValidationMixin` on the link form, `ScopedFilterMixin`/`TenancyFilterMixin`/`DistanceFilterMixin` on GraphQL filters, `TenancyColumnsMixin` on tables. [fg:symbols:wireless.models:WirelessLAN] [fg:symbols:wireless.models:WirelessLink] [fg:symbols:wireless.filtersets:WirelessLANFilterSet] [fg:symbols:wireless.forms.model_forms:WirelessLANForm] [fg:symbols:wireless.forms.model_forms:WirelessLinkForm] [fg:symbols:wireless.graphql.filters:WirelessLinkFilter] [fg:symbols:wireless.tables.wirelesslink:WirelessLinkTable]

Mixin order is consistent: the feature mixin comes first and the NetBox base class last (`ScopedForm, TenancyForm, NetBoxModelForm`; `ScopedBulkEditForm, NetBoxModelBulkEditForm`; `TenancyColumnsMixin, NetBoxTable`). [code:netbox/wireless/forms/model_forms.py:41] [code:netbox/wireless/forms/bulk_edit.py:44] [code:netbox/wireless/tables/wirelesslan.py:42]

The one piece of behaviour that is local is `WirelessLink.clean()`/`save()`: it validates both interface types against `dcim.constants.WIRELESS_IFACE_TYPES` and copies each interface's device into the `_interface_*_device` cache columns. [code:netbox/wireless/models.py:197-219]

## P3. Shared attribute groups are expressed as abstract mixins at every layer

The auth triple (`auth_type`, `auth_cipher`, `auth_psk`) is defined once in `WirelessAuthenticationBase` and inherited by both primary models; the GraphQL side mirrors this with `WirelessAuthenticationBaseFilterMixin`, applied to both `WirelessLANFilter` and `WirelessLinkFilter`. [code:netbox/wireless/models.py:20-45] [code:netbox/wireless/graphql/filter_mixins.py:18-26] [code:netbox/wireless/graphql/filters.py:32-37] [code:netbox/wireless/graphql/filters.py:51-56]

Exception: REST serializers, django-filter filtersets and Django forms do not have such a mixin; the three auth fields are re-declared by hand in every one of them (two serializers, two filtersets, two bulk-edit forms, two import forms, two filter forms), and `auth_psk` gets a `PasswordInput(render_value=True, attrs={'data-toggle': 'password'})` widget declared identically in both model forms. [code:netbox/wireless/api/serializers_/wirelesslans.py:39-40] [code:netbox/wireless/api/serializers_/wirelesslinks.py:20-21] [code:netbox/wireless/filtersets.py:69-74] [code:netbox/wireless/filtersets.py:100-105] [code:netbox/wireless/forms/model_forms.py:69-74] [code:netbox/wireless/forms/model_forms.py:186-191]

## P4. Choice sets are the single source of enums; other layers derive from them

`choices.py` holds `ChoiceSet` subclasses; every other representation is derived: `status` fields point at `WirelessLANStatusChoices`, GraphQL enums are produced by `strawberry.enum(X.as_enum(prefix=...))`, forms wrap them with `add_blank_choice`, import forms use `CSVChoiceField(choices=...)`, and `get_status_color` reads `.colors`. Only `WirelessLANStatusChoices` declares a `key` (`'WirelessLAN.status'`), making it the one user-overridable choice set in the app. [code:netbox/wireless/choices.py:16-29] [code:netbox/wireless/graphql/enums.py:13-17] [code:netbox/wireless/forms/filtersets.py:51-55] [code:netbox/wireless/forms/bulk_import.py:44-48] [code:netbox/wireless/models.py:122-123]

Exception: `WirelessLink.status` does not use a wireless choice set at all; it reuses `dcim.choices.LinkStatusChoices` (default `STATUS_CONNECTED`) in the model, serializer, filterset, and all three form types. [code:netbox/wireless/models.py:147-152] [code:netbox/wireless/api/serializers_/wirelesslinks.py:16] [code:netbox/wireless/filtersets.py:97-99] [code:netbox/wireless/forms/bulk_edit.py:108-112]

Exception (bug-shaped): `WirelessLinkFilter.status` in GraphQL is typed as `WirelessLANStatusEnum`, not a link-status enum, so the GraphQL filter vocabulary for links disagrees with the model's `LinkStatusChoices`. [code:netbox/wireless/graphql/filters.py:66-68] [code:netbox/wireless/models.py:150]

## P5. Wireless channels are encoded strings, decoded on demand

`WirelessChannelChoices` values pack `band-id-frequency-width` into one string (e.g. `'2.4g-1-2412-22'`, `'5g-50-5250-160'`), grouped in `CHOICES` by band label. `get_channel_attr` is the only decoder and is consumed by `dcim.Interface` to validate and back-fill `rf_channel_frequency`/`rf_channel_width`. [code:netbox/wireless/choices.py:32-59] [code:netbox/wireless/choices.py:239-243] [code:netbox/wireless/utils.py:11-28] [code:netbox/dcim/models/device_components.py:962-967]

## P6. Cross-app FKs use `PROTECT`; caches use `CASCADE`/`SET_NULL`

User-facing relations to other apps protect the referenced object: `vlan`, `tenant`, `interface_a`, `interface_b` are all `on_delete=PROTECT`. Internal cache/denormalisation columns cascade or null instead: `_interface_a_device`/`_interface_b_device` cascade on `dcim.Device`, `WirelessLAN.group` is `SET_NULL`, and `dcim.Interface.wireless_link` back-pointer is `SET_NULL`. [fg:model_refs:wireless.models:97] [fg:model_refs:wireless.models:130] [code:netbox/wireless/models.py:97-110] [code:netbox/wireless/models.py:163-176] [code:netbox/wireless/models.py:84-90] [code:netbox/dcim/models/device_components.py:742-748]

Where a relation must not create a reverse accessor, `related_name='+'` is used: both link interfaces and both device caches on `WirelessLink`, and `Interface.wireless_link` in `dcim`. [code:netbox/wireless/models.py:130-141] [code:netbox/wireless/models.py:163-176] [code:netbox/dcim/models/device_components.py:742-748]

## P7. Model-to-interface consistency is maintained by signals, not by the model

`WirelessLink` never touches `Interface.wireless_link` in `save()`; the `post_save` receiver sets it on both endpoints (and skips when `raw=True` for fixtures) and calls `create_cablepath` for each on creation, converting `UnsupportedCablePath` into `AbortRequest`; the `post_delete` receiver nulls the pointers with a queryset `update()` and deletes any `CablePath` containing the link. [code:netbox/wireless/signals.py:17-42] [code:netbox/wireless/signals.py:45-61]

Exception (asymmetry): the save receiver compares `interface_a.wireless_link != instance` but `interface_b.cable != instance`, so side B is re-saved on every save rather than only when stale. [code:netbox/wireless/signals.py:27-34]

## P8. Views are declarative, registered by decorator, and URLs are generated

All 21 views only assign `queryset`, `filterset`, `filterset_form`, `table`, `form`/`model_form`; the sole custom logic is `get_extra_context` on the two detail views (descendant-aware related models for groups; a restricted interfaces table for LANs). `urls.py` is entirely `get_model_urls(...)` includes and `api/urls.py` entirely router registrations. [code:netbox/wireless/views.py:27-36] [code:netbox/wireless/views.py:98-111] [code:netbox/wireless/urls.py:7-18] [code:netbox/wireless/api/urls.py:5-13]

Group counts are annotated with the same `add_related_count(..., WirelessLAN, 'group', 'wirelesslan_count', cumulative=True)` call in the group list, bulk-edit, bulk-delete views and the API viewset. [code:netbox/wireless/views.py:15-21] [code:netbox/wireless/views.py:59-65] [code:netbox/wireless/api/views.py:18-24]

## P9. Location scoping and region/site cascades reuse dcim's cached-scope machinery

`WirelessLAN` gets `scope_type`/`scope_id`/`scope` plus `_region/_site_group/_site/_location` from `CachedScopeMixin`; the filterset adds `region_id`/`site_id`/... via `ScopedFilterSet` on those cache columns; the serializer limits `scope_type` to `LOCATION_SCOPE_TYPES` and resolves `scope` with `get_serializer_for_model`; the GraphQL type excludes the raw cache columns and exposes `scope` as a `WirelessLANScopeType` union. `WirelessLink` has no scope at all. [fg:imports:wireless.models->dcim.models.mixins] [code:netbox/dcim/base_filtersets.py:13-23] [code:netbox/wireless/api/serializers_/wirelesslans.py:41-67] [code:netbox/wireless/graphql/types.py:35-55] [code:netbox/wireless/models.py:126]

## P10. Link endpoints are chosen by a site -> location -> device -> interface chain

The model form declares four `DynamicModelChoiceField`s per side (`site_a`, `location_a`, `device_a`, `interface_a`), chained by `query_params` (`$site_a`, `$device_a`) with `initial_params` for reverse population, `kind: 'wireless'` restricting to wireless interface types, and `context={'disabled': '_occupied'}` greying out already-linked interfaces. The import form implements the same narrowing manually in `__init__` for both sides. [code:netbox/wireless/forms/model_forms.py:78-119] [code:netbox/wireless/forms/model_forms.py:120-161] [code:netbox/wireless/forms/bulk_import.py:169-189] [code:netbox/dcim/filtersets.py:2007-2013]

## P11. Nullable choice fields store NULL, not empty string

`auth_type`, `auth_cipher` and `distance_unit` are `blank=True, null=True`; migration 0010 altered the columns and ran a data step replacing `''` with `NULL`. Serializers pair `allow_blank=True` on auth fields with `allow_null=True` only on `distance_unit`. [code:netbox/wireless/models.py:24-37] [code:netbox/wireless/migrations/0010_charfield_null_choices.py:4-16] [code:netbox/wireless/api/serializers_/wirelesslinks.py:20-22]

## P12. Tests are inherited suites plus fixture data

Each test class subclasses a shared suite (`APIViewTestCases.APIViewTestCase`, `ChangeLoggedFilterSetTests`, `ViewTestCases.OrganizationalObjectViewTestCase`/`PrimaryObjectViewTestCase`) and supplies only `setUpTestData`, `form_data`, `csv_data`, plus one `test_<field>` per filter. There are no model-method tests for `WirelessLink.clean()` interface-type validation or for `get_channel_attr` inside this app. [fg:symbols:wireless.tests.test_api:WirelessLANTest] [fg:symbols:wireless.tests.test_filtersets:WirelessLinkTestCase] [fg:symbols:wireless.tests.test_views:WirelessLANTestCase] [code:netbox/wireless/tests/test_views.py:11-40] [fg:subsystems:wireless]
