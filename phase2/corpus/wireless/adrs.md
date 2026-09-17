# wireless — retro-ADRs (T0 ea4c205)

## ADR-W1. Wireless links are a separate model from Cable, but participate in dcim path tracing

**Context.** A wireless point-to-point link connects two interfaces like a cable does, but has no physical terminations, no length/colour, and carries SSID and authentication attributes. NetBox already had `Cable` and `CablePath` in `dcim`. [code:netbox/wireless/models.py:126-146] [fg:imports:wireless.signals->dcim.models]

**Decision.** `WirelessLink` is its own `PrimaryModel` in a separate app with exactly two `PROTECT` FKs (`interface_a`, `interface_b`) and a unique constraint on the pair; `dcim` was extended to recognise it as a link kind: `Interface.wireless_link` is a nullable FK back to it, `Interface.link` returns `cable or wireless_link`, `link_peers` returns the opposite interface, `CablePath.from_origin` accepts `Cable` or `WirelessLink`, and the SVG tracer draws it with a `wireless-link` class. [fg:model_refs:wireless.models:130] [fg:model_refs:wireless.models:136] [code:netbox/wireless/models.py:182-187] [fg:model_refs:dcim.models.device_components:742] [code:netbox/dcim/models/device_components.py:995-1008] [code:netbox/dcim/models/cables.py:576-577] [code:netbox/dcim/svg/cables.py:95-97]

**Consequences.** `dcim` and `wireless` are mutually dependent: 27 of the 33 inbound import edges come from `dcim`, and `dcim.models.cables` imports `wireless.models` while `wireless.models` imports `dcim.choices`/`dcim.constants`. Interface occupancy (`_occupied`, `filter_occupied`) must check both `cable` and `wireless_link`. Link status vocabulary is borrowed from `dcim.choices.LinkStatusChoices` rather than defined locally. [fg:subsystems:wireless] [fg:imports:dcim.models.cables->wireless.models] [fg:imports:wireless.models->dcim.choices] [code:netbox/dcim/models/device_components.py:971-973] [code:netbox/dcim/filtersets.py:2016-2027] [code:netbox/wireless/models.py:147-152]

## ADR-W2. Interface back-pointers and cable paths are maintained by signal receivers

**Context.** After a `WirelessLink` is created the two interfaces must point at it and `CablePath`s must exist so tracing works; after deletion they must be cleared. This is the same bookkeeping `Cable` needs. [code:netbox/wireless/signals.py:19-21] [code:netbox/wireless/signals.py:47-49]

**Decision.** The model's `save()` only populates the device cache columns; the cross-model writes live in `wireless/signals.py` as `post_save`/`post_delete` receivers imported for side effect in `WirelessConfig.ready()`. The save receiver bails out for `raw` loads, re-saves each endpoint interface, and on creation calls `dcim.utils.create_cablepath` per interface, translating `UnsupportedCablePath` into `AbortRequest`. The delete receiver uses `Interface.objects.filter(...).update(wireless_link=None)` (bypassing interface save signals) and deletes `CablePath`s whose `_nodes` contain the link. [code:netbox/wireless/models.py:214-219] [code:netbox/wireless/signals.py:17-42] [code:netbox/wireless/signals.py:45-61] [code:netbox/wireless/apps.py:7-12]

**Consequences.** Endpoint consistency depends on the app being loaded and on signals firing; bulk `QuerySet.update()`/`delete()` on links will not maintain it. The B-side staleness check compares against `interface_b.cable` instead of `.wireless_link`, so interface B is always re-saved. [code:netbox/wireless/apps.py:9] [code:netbox/wireless/signals.py:27-34]

## ADR-W3. Denormalise each link endpoint's Device onto the link

**Context.** Filtering or grouping links by device would otherwise require joining through `Interface`. [code:netbox/wireless/models.py:161-162]

**Decision.** `WirelessLink` carries `_interface_a_device` and `_interface_b_device` (CASCADE FKs to `dcim.Device`, `related_name='+'`), populated unconditionally in `save()` from `interface_a.device`/`interface_b.device`; the underscore marks them as internal. [fg:model_refs:wireless.models:163] [fg:model_refs:wireless.models:170] [code:netbox/wireless/models.py:163-176] [code:netbox/wireless/models.py:214-219]

**Consequences.** Deleting a device cascades to its links (while deleting an interface is blocked by `PROTECT`). The stated purpose is not yet realised in this app: `WirelessLinkFilterSet` exposes no `device_id` filter, and the only reader of the cache columns outside the model is the GraphQL type, which exposes them verbatim as `_interface_a_device`/`_interface_b_device`. [code:netbox/wireless/models.py:130-141] [code:netbox/wireless/filtersets.py:90-109] [code:netbox/wireless/graphql/types.py:64-69]

## ADR-W4. WirelessLAN is scoped to a location via a generic FK plus cached FKs (replacing no scope at all)

**Context.** LANs originally had no geographic placement; users needed to see LANs per region, site group, site or location, and `dcim` had introduced `CachedScopeMixin` for exactly this (`dcim` migration `0196_qinq_svlan` is the dependency of the wireless scope migration). [code:netbox/wireless/migrations/0011_wirelesslan__location_wirelesslan__region_and_more.py:8-12] [code:netbox/dcim/models/mixins.py:37-41]

**Decision.** In migration 0011 (2024-11) `WirelessLAN` gained `scope_type`/`scope_id` and four cache FKs `_region/_site_group/_site/_location`; 0012 immediately dropped their `related_name`. Every layer reuses dcim's scoped mixins: `ScopedFilterSet`, `ScopedForm`, `ScopedBulkEditForm`, `ScopedImportForm`, `ScopedFilterMixin`; the serializer restricts `scope_type` to `LOCATION_SCOPE_TYPES`; `scope_type` and `scope_id` are in `clone_fields`. [code:netbox/wireless/migrations/0011_wirelesslan__location_wirelesslan__region_and_more.py:14-24] [code:netbox/wireless/migrations/0012_alter_wirelesslan__location_and_more.py:14-19] [fg:imports:wireless.filtersets->dcim.base_filtersets] [fg:imports:wireless.forms.bulk_edit->dcim.forms.mixins] [fg:imports:wireless.graphql.filters->dcim.graphql.filter_mixins] [code:netbox/wireless/api/serializers_/wirelesslans.py:41-48] [code:netbox/wireless/models.py:112]

**Consequences.** `dcim` detail views for Region/SiteGroup/Site/Location query `WirelessLAN` directly on the cache columns, adding a second inbound dependency path from `dcim.views`. The GraphQL type must explicitly exclude the four cache columns and `scope_type`/`scope_id`, and re-expose `scope` as a four-way union. `WirelessLink` was deliberately left unscoped. [fg:imports:dcim.views->wireless.models] [code:netbox/dcim/views.py:265] [code:netbox/wireless/graphql/types.py:35-55] [code:netbox/wireless/models.py:126]

## ADR-W5. Channel data is encoded in the choice value, not in a table

**Context.** Wireless interfaces need channel number, centre frequency and width per band; NetBox has no model for RF channel plans. [code:netbox/dcim/models/device_components.py:699-720]

**Decision.** `WirelessChannelChoices` encodes `band-id-frequency-width` into each value string (over 190 entries across 2.4/5/6/60 GHz), grouped by band in `CHOICES`; `wireless.utils.get_channel_attr` parses the string. `dcim.Interface` stores the channel string in `rf_channel` and separately stores `rf_channel_frequency`/`rf_channel_width`, back-filled from the channel in `save()` and cross-checked in `clean()`. [code:netbox/wireless/choices.py:32-36] [code:netbox/wireless/choices.py:239-243] [code:netbox/wireless/utils.py:11-28] [code:netbox/dcim/models/device_components.py:936-946] [code:netbox/dcim/models/device_components.py:962-967]

**Consequences.** `choices.py` is the largest module in the app (484 LOC) and a compile-time dependency of `dcim` models, templates, serializers, filtersets, forms and tests; adding a channel is a code change plus a `dcim` migration-free choices edit, and any typo in an encoded value only surfaces when `get_channel_attr` splits it. [fg:modules:wireless.choices] [fg:imports:dcim.models.device_components->wireless.choices] [fg:imports:dcim.models.device_components->wireless.utils] [fg:imports:dcim.forms.bulk_import->wireless.choices]

## ADR-W6. Authentication attributes are an abstract model shared by LAN and Link

**Context.** Both a broadcast LAN and a point-to-point link need auth type, cipher and PSK, with a PSK length cap of 64 and an SSID cap of 32 per IEEE 802.11. [code:netbox/wireless/constants.py:1-2]

**Decision.** `WirelessAuthenticationBase` (abstract) carries the three fields; both models inherit it first in their MRO; GraphQL mirrors it with `WirelessAuthenticationBaseFilterMixin`. `auth_psk` is stored as plain text (a `CharField`, no encryption), rendered through a password-toggle widget in forms, and is searchable in the global search index at weight 2000. [code:netbox/wireless/models.py:20-45] [code:netbox/wireless/models.py:76] [code:netbox/wireless/graphql/filter_mixins.py:18-26] [code:netbox/wireless/forms/model_forms.py:69-74] [code:netbox/wireless/search.py:5-13]

**Consequences.** Adding an auth attribute is one model edit but still requires manual edits in two serializers, two filtersets and six form classes, because no shared mixin exists at those layers. The PSK is exposed in REST, GraphQL (`fields='__all__'` on links), tables and filters like any other field. [code:netbox/wireless/api/serializers_/wirelesslinks.py:26-30] [code:netbox/wireless/graphql/types.py:58-63] [code:netbox/wireless/tables/wirelesslink.py:46-50] [code:netbox/wireless/filtersets.py:107-109]

## ADR-W7. Empty choice values are NULL, and nullable enums are surfaced as such

**Context.** Optional `CharField` choices were originally stored as `''`, which conflicts with `allow_null` semantics in the API and with GraphQL enums. [code:netbox/wireless/migrations/0010_charfield_null_choices.py:19-49]

**Decision.** Migration 0010 made `auth_type`, `auth_cipher` (both models) and `distance_unit` nullable and converted existing `''` to `NULL` via `RunPython` with a no-op reverse. Model fields declare `blank=True, null=True`. [code:netbox/wireless/migrations/0010_charfield_null_choices.py:4-16] [code:netbox/wireless/migrations/0010_charfield_null_choices.py:50] [code:netbox/wireless/models.py:24-37]

**Consequences.** The migration is irreversible in data terms; serializers must accept blank and, for `distance_unit`, null, and every filter form uses `add_blank_choice`. [code:netbox/wireless/api/serializers_/wirelesslinks.py:20-22] [code:netbox/wireless/forms/filtersets.py:115-124]

## ADR-W8. Migration history squashed to a single baseline

**Context.** Eight incremental migrations from the app's 2021 introduction through 2023 (tenancy, id standardisation, unique constraints, status field). [code:netbox/wireless/migrations/0001_squashed_0008.py:10-19]

**Decision.** `0001_squashed_0008` replaces them and depends on the squashed baselines of `ipam`, `tenancy`, `extras` and `dcim`. [code:netbox/wireless/migrations/0001_squashed_0008.py:21-25] [fg:churn:wireless.migrations.0001_squashed_0008]

**Consequences.** Post-squash migrations (0009-0015) are the readable history of the app's evolution: distance (2024-06), null choices, location scope (2024-11), natural-sort collation on group name (depends on `dcim 0197`), group comments, widened `_abs_distance` (2025-05). [code:netbox/wireless/migrations/0013_natural_ordering.py:5-8] [code:netbox/wireless/migrations/0015_extend_wireless_link_abs_distance_upper_limit.py:11-15]

## ADR-W9. WirelessLANGroup is an MPTT tree with advisory-locked API writes

**Context.** Groups nest; concurrent MPTT inserts through the API can corrupt tree fields. [code:netbox/netbox/api/viewsets/__init__.py:214-218]

**Decision.** `WirelessLANGroup` extends `NestedGroupModel` with a `(parent, name)` unique constraint and a natural-sort collation on `name`; the API viewset adds `MPTTLockedMixin`, keyed by `'wirelesslangroup'` in `ADVISORY_LOCK_KEYS`; counts are annotated cumulatively over descendants. [code:netbox/wireless/models.py:48-73] [code:netbox/wireless/api/views.py:17-24] [code:netbox/netbox/constants.py:23] [code:netbox/wireless/views.py:15-21]

**Consequences.** UI edit views do not take the lock (only the API viewset does), and the group detail view aggregates related models across `get_descendants(include_self=True)`. [code:netbox/wireless/views.py:39-43] [code:netbox/wireless/views.py:27-36]
