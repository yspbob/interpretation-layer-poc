# circuits — patterns and conventions (NetBox @ ea4c205)

## Model layering

**Three model tiers, chosen by role.** First-class objects (Provider, ProviderAccount, ProviderNetwork, Circuit, VirtualCircuit) extend `PrimaryModel`; categorising objects (CircuitType, VirtualCircuitType via `BaseCircuitType`, CircuitGroup) extend `OrganizationalModel`; child and junction objects (CircuitTermination, CircuitGroupAssignment, VirtualCircuitTermination) extend `ChangeLoggedModel` and opt into features one mixin at a time. [code:netbox/circuits/models/providers.py:15] [code:netbox/circuits/models/circuits.py:38] [code:netbox/circuits/models/base.py:11] [code:netbox/circuits/models/circuits.py:179] [code:netbox/circuits/models/circuits.py:231-237] [code:netbox/circuits/models/virtual_circuits.py:121-126]

**ChangeLoggedModel-based classes define `get_absolute_url` themselves**, because only `NetBoxFeatureSet` supplies it; all three do, and no PrimaryModel/OrganizationalModel subclass does. [code:netbox/netbox/models/__init__.py:45] [code:netbox/circuits/models/circuits.py:227-228] [code:netbox/circuits/models/circuits.py:344-345] [code:netbox/circuits/models/virtual_circuits.py:157-158]

**Child objects report their parent for change logging** via `to_objectchange()` setting `related_object` and a `parent_object` property. [code:netbox/circuits/models/circuits.py:380-387] [code:netbox/circuits/models/virtual_circuits.py:163-170]

**on_delete follows ownership.** Owner references (provider, type, tenant, ContentType) are PROTECT; parent→child links (termination.circuit, assignment.group, virtual termination.interface) are CASCADE; cache FKs are SET_NULL or CASCADE. [code:netbox/circuits/models/circuits.py:49-65] [code:netbox/circuits/models/circuits.py:238-242] [code:netbox/circuits/models/circuits.py:195-199] [code:netbox/circuits/models/circuits.py:97-104]

**Scoped uniqueness via named `UniqueConstraint`s** using the `%(app_label)s_%(class)s_unique_...` template: Circuit (provider, cid) and (provider_account, cid); VirtualCircuit (provider_network, cid); ProviderAccount with a conditional constraint on non-empty name; CircuitTermination (circuit, term_side); CircuitGroupAssignment (member_type, member_id, group). [code:netbox/circuits/models/circuits.py:132-141] [code:netbox/circuits/models/virtual_circuits.py:89-98] [code:netbox/circuits/models/providers.py:72-82] [code:netbox/circuits/models/circuits.py:332-337]

**`clone_fields` and `prerequisite_models` are declared on primary models**; Provider deliberately sets `clone_fields = ()`. [code:netbox/circuits/models/circuits.py:121-128] [code:netbox/circuits/models/virtual_circuits.py:79-85] [code:netbox/circuits/models/providers.py:38]

**Cross-model invariants live in `clean()`**: an account must belong to the circuit's provider; a virtual circuit's account must belong to its network's provider; a termination must have a target; a virtual termination's interface must be virtual. [code:netbox/circuits/models/circuits.py:151-155] [code:netbox/circuits/models/virtual_circuits.py:108-114] [code:netbox/circuits/models/circuits.py:347-351] [code:netbox/circuits/models/virtual_circuits.py:187-191]

## Generic relations with a closed allowlist

**GFK plus constant allowlist.** Both GenericForeignKeys (`CircuitTermination.termination`, `CircuitGroupAssignment.member`) are constrained by a constant in `constants.py`, and that constant is reused verbatim as a ContentType queryset in the model form, bulk-edit form, import form and serializer. [code:netbox/circuits/constants.py:5-12] [code:netbox/circuits/forms/model_forms.py:167-172] [code:netbox/circuits/forms/model_forms.py:256-261] [code:netbox/circuits/forms/bulk_import.py:136-140] [code:netbox/circuits/api/serializers_/circuits.py:157-159]

**HTMX-driven GFK forms follow one recipe**: a `ContentTypeChoiceField` with `HTMXSelect`, a disabled `DynamicModelChoiceField` with an empty initial queryset, an `__init__` that seeds `initial` from the instance and re-enables the field using `get_field_value`, and a `clean()` that assigns the object onto `self.instance`. Three forms implement it. [code:netbox/circuits/forms/model_forms.py:205-233] [code:netbox/circuits/forms/model_forms.py:280-307] [code:netbox/circuits/forms/bulk_edit.py:249-261]

**Serializers expose GFK targets through `SerializerMethodField` + `get_serializer_for_model(..., nested=True)`**, identical in three places. [code:netbox/circuits/api/serializers_/circuits.py:65-71] [code:netbox/circuits/api/serializers_/circuits.py:147-153] [code:netbox/circuits/api/serializers_/circuits.py:170-176]

**GraphQL types exclude the raw `*_type`/`*_id` columns and expose a `strawberry.union` field** whose members are the allowlisted types. [code:netbox/circuits/graphql/types.py:70-87] [code:netbox/circuits/graphql/types.py:129-143]

**Reverse access from members uses `GenericRelation` with `related_query_name`**, so Circuit and VirtualCircuit both filter as `circuit`/`virtual_circuit` on assignments. [code:netbox/circuits/models/circuits.py:114-119] [code:netbox/circuits/models/virtual_circuits.py:72-77]

## Denormalised caches

**Underscore-prefixed cache FKs are recomputed in `save()` and are the only thing filters and tables read.** `cache_related_objects()` fills `_region/_site_group/_site/_location/_provider_network`; filtersets, tables and dcim views query those fields rather than the GFK. [code:netbox/circuits/models/circuits.py:353-378] [code:netbox/circuits/filtersets.py:280-334] [code:netbox/circuits/tables/circuits.py:127-152] [code:netbox/dcim/views.py:474-482]

**Cache maintenance by signal, not by caller**: `Circuit.termination_a/_z` are `editable=False` and set by the `post_save` receiver; `DistanceMixin` similarly maintains `_abs_distance`. [code:netbox/circuits/models/circuits.py:96-112] [code:netbox/circuits/signals.py:8-15] [code:netbox/netbox/models/mixins.py:72-87]

## Views and URLs

**One class per model per action, registered with `@register_model_view`, routed with `get_model_urls`.** Provider, ProviderAccount, ProviderNetwork, CircuitType, Circuit, CircuitTermination, CircuitGroup, CircuitGroupAssignment and VirtualCircuitType all follow it. [code:netbox/circuits/views.py:20-63] [code:netbox/circuits/views.py:226-281] [code:netbox/circuits/urls.py:8-18]

**Detail views for organisational/provider objects use `GetRelatedModelsMixin`** and pass `extra` querysets when the relation is indirect (VirtualCircuit via provider network; Circuit via cached provider network on terminations). [code:netbox/circuits/views.py:33-51] [code:netbox/circuits/views.py:166-186]

**Counts are annotated in the view with `count_related`, rendered by `LinkedCountColumn`, and exposed in the API by `RelatedObjectCountField`.** [code:netbox/circuits/views.py:22-26] [code:netbox/circuits/tables/providers.py:39-44] [code:netbox/circuits/api/serializers_/providers.py:33] [code:netbox/circuits/api/serializers_/circuits.py:35]

**Bulk import with nested children** uses a form triplet (plain `ModelForm` base → `ImportRelatedForm` → `ImportForm(NetBoxModelImportForm)`) and a `BulkImportView` declaring `related_object_forms`, `additional_permissions` and `prep_related_object_data`; done identically for Circuit and VirtualCircuit, each with a dedicated test. [code:netbox/circuits/forms/bulk_import.py:126-165] [code:netbox/circuits/forms/bulk_import.py:247-280] [code:netbox/circuits/views.py:314-327] [code:netbox/circuits/views.py:676-688] [code:netbox/circuits/tests/test_views.py:199-247]

## Filtersets, tables, API, GraphQL

**Filter pairs `<name>_id` (pk) / `<name>` (slug or natural key)** on `ModelMultipleChoiceFilter`; hierarchical dcim objects use `TreeNodeMultipleChoiceFilter` with `lookup_expr='in'`; every filterset defines `search()` as an OR of `icontains` Qs. [code:netbox/circuits/filtersets.py:99-108] [code:netbox/circuits/filtersets.py:200-225] [code:netbox/circuits/filtersets.py:257-267] [code:netbox/circuits/filtersets.py:524-531]

**Virtual circuits derive the provider through the network**: a `provider` property on the model, `provider_network__provider` accessors in filters and tables. [code:netbox/circuits/models/virtual_circuits.py:116-118] [code:netbox/circuits/filtersets.py:479-489] [code:netbox/circuits/tables/virtual_circuits.py:44-48]

**Filter forms mirror filtersets, group fields in named `FieldSet`s, chain dependent selects with `query_params`, and end with `tag = TagFilterField(model)`.** [code:netbox/circuits/forms/filtersets.py:121-160] [code:netbox/circuits/forms/filtersets.py:34-40] [code:netbox/circuits/forms/filtersets.py:217]

**Serializers nest related objects with `Serializer(nested=True)`, list `brief_fields`, and `ChoiceField` for ChoiceSets.** [code:netbox/circuits/api/serializers_/circuits.py:102-121] [code:netbox/circuits/api/serializers_/circuits.py:193-206] [code:netbox/circuits/api/serializers_/providers.py:44-54]

**GraphQL types are `fields='__all__'` with explicit relation annotations using `strawberry.lazy` to avoid import cycles;** the schema exposes `<model>` and `<model>_list` per type. [code:netbox/circuits/graphql/types.py:32-43] [code:netbox/circuits/graphql/types.py:175-189] [code:netbox/circuits/graphql/schema.py:9-42]

**ChoiceSets that users may extend carry a `key`** (status, commit rate, port speed, priority); structural ones (side, role) do not. Colour is the third tuple element and surfaces via `get_status_color`/`get_role_color`. [code:netbox/circuits/choices.py:10-27] [code:netbox/circuits/choices.py:52-60] [code:netbox/circuits/choices.py:101-110] [code:netbox/circuits/models/virtual_circuits.py:160-161]

**Module hygiene**: every module lists `__all__`; package `__init__` files re-export by star import (models, forms, tables, api.serializers). [code:netbox/circuits/models/__init__.py:1-3] [code:netbox/circuits/api/serializers.py:1-2] [code:netbox/circuits/filtersets.py:17-29]

**Schema migrations that reshape change-logged data ship an `objectchange_migrators` hook** alongside a `RunPython` data step (0047, 0048, 0051). [code:netbox/circuits/migrations/0047_circuittermination__termination.py:55-75] [code:netbox/circuits/migrations/0048_circuitterminations_cached_relations.py:91-100] [code:netbox/circuits/migrations/0051_virtualcircuit_group_assignment.py:88-103]

**Tests: one case per model per layer**, built on `APIViewTestCases`, `ViewTestCases.PrimaryObjectViewTestCase`/`OrganizationalObjectViewTestCase`, and `ChangeLoggedFilterSetTests`. [code:netbox/circuits/tests/test_api.py:20] [code:netbox/circuits/tests/test_views.py:18] [code:netbox/circuits/tests/test_views.py:69] [code:netbox/circuits/tests/test_filtersets.py:16]

## Exceptions

- **Virtual-circuit list and bulk views are not decorator-registered**; `urls.py` wires them by explicit `path()`, unlike every other model. The swap view is also explicit. [code:netbox/circuits/views.py:651] [code:netbox/circuits/views.py:676] [code:netbox/circuits/urls.py:37-43] [code:netbox/circuits/urls.py:48-74]
- **VirtualCircuitTermination is treated as cabled in the API but not in the model**: its serializer inherits `CabledObjectSerializer` and its viewset mixes in `PassThroughPortMixin`, while the model is not a `CabledObjectModel` and the GraphQL type omits `CabledObjectMixin`. [code:netbox/circuits/api/serializers_/circuits.py:209] [code:netbox/circuits/api/views.py:122] [code:netbox/circuits/models/virtual_circuits.py:121-126] [code:netbox/circuits/graphql/types.py:164]
- **Contacts columns/filters appear on VirtualCircuit** (`ContactsColumnMixin`, `ContactModelFilterForm`) although the model lacks `ContactsMixin` and the filterset lacks `ContactModelFilterSet`. [code:netbox/circuits/tables/virtual_circuits.py:39] [code:netbox/circuits/forms/filtersets.py:326] [code:netbox/circuits/models/virtual_circuits.py:32] [code:netbox/circuits/filtersets.py:478]
- **`provider_account` natural-key filters on Circuit and VirtualCircuit use `Provider.objects` with `to_field_name='account'`**, whereas the VirtualCircuitTermination version uses `ProviderAccount.objects`. [code:netbox/circuits/filtersets.py:175-180] [code:netbox/circuits/filtersets.py:495-500] [code:netbox/circuits/filtersets.py:563-568]
- **VirtualCircuitType bulk views annotate `count_related(Circuit, 'type')`** while its list view and table use `VirtualCircuit`. [code:netbox/circuits/views.py:592-594] [code:netbox/circuits/views.py:630-632] [code:netbox/circuits/views.py:640-642]
- `termination_z_id` is labelled "Termination A (ID)". [code:netbox/circuits/filtersets.py:246-249]
- `CircuitTermination` declares its own `description` field rather than inheriting one, since it is not a PrimaryModel. [code:netbox/circuits/models/circuits.py:287-291]
