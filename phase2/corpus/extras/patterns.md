# extras — patterns and conventions (NetBox ea4c205)

## 1. Object-type targeting: `object_types` M2M for configuration, GenericForeignKey for attachment

Models that *apply to* kinds of objects carry an `object_types = ManyToManyField(to='core.ObjectType', related_name=...)`: EventRule, CustomLink, ExportTemplate, SavedFilter, CustomField, Tag. [fg:model_refs:extras.models.models:51] [fg:model_refs:extras.models.models:292] [fg:model_refs:extras.models.models:453] [fg:model_refs:extras.models.customfields:74] [fg:model_refs:extras.models.tags:37]

Models that *attach to one object* use an FK to `contenttypes.ContentType` plus `object_id` and a `GenericForeignKey`, always with a composite `Index(fields=('object_type', 'object_id'))`: ImageAttachment, JournalEntry, Bookmark, Notification, Subscription, CachedValue. [code:netbox/extras/models/models.py:648-656] [code:netbox/extras/models/models.py:678-682] [code:netbox/extras/models/models.py:770-774] [code:netbox/extras/models/notifications.py:52-60] [code:netbox/extras/models/notifications.py:212-216] [code:netbox/extras/models/search.py:26-35]

Exception: `TableConfig.object_type` is a single FK to `core.ObjectType` (one table config per table type) rather than an M2M, and `EventRule.action_object_type` targets `contenttypes.ContentType` because it points at the action target, not an applicable type. [fg:model_refs:extras.models.models:533] [fg:model_refs:extras.models.models:89]

## 2. Feature gating through `ObjectType.objects.with_feature()` at every boundary

The set of object types a feature can target is computed from the registry, never hard-coded: forms, CSV import forms, filter forms, serializers and model `clean()` all call `ObjectType.objects.with_feature('<feature>')`. [code:netbox/extras/forms/model_forms.py:48-52] [code:netbox/extras/forms/bulk_import.py:36-39] [code:netbox/extras/api/serializers_/customfields.py:39-43] [code:netbox/extras/models/models.py:692-699] [code:netbox/extras/models/notifications.py:93-100] [code:netbox/extras/models/models.py:844-851]

The feature names are the keys of `FEATURES_MAP` in `netbox.models.features`, populated when `ExtrasConfig.ready()` calls `register_models()`. [code:netbox/netbox/models/features.py:618-634] [code:netbox/extras/apps.py:7-12]

Exception: `CustomField.related_object_type` and the SavedFilter/TableConfig filter forms use `ObjectType.objects.public()` because any public model may be referenced, not only feature-bearing ones. [code:netbox/extras/forms/model_forms.py:57-61] [code:netbox/extras/forms/filtersets.py:234-237]

## 3. Runtime dispatch through `netbox.registry`, not static tables

Whether an object participates in event rules or notifications is checked against `registry['model_features']` at signal time; event-type choices come from `registry['event_types']`; dashboard widgets are looked up in `registry['widgets']`; `ConfigTemplate.get_context` exposes every registered model from `registry['models']`. [code:netbox/extras/events.py:58-62] [code:netbox/extras/signals.py:152-155] [code:netbox/extras/models/notifications.py:24-31] [code:netbox/extras/dashboard/utils.py:29-36] [code:netbox/extras/models/configs.py:241-256]

## 4. Two base-class tiers, chosen by whether the model has custom fields and tags

EventRule, Webhook and JournalEntry mix in `CustomFieldsMixin`+`TagsMixin`, so their serializers are `NetBoxModelSerializer`, their forms `NetBoxModelForm`, their import forms `NetBoxModelImportForm`, their filtersets `NetBoxModelFilterSet`, and their GraphQL types carry `CustomFieldsMixin, TagsMixin` or `OrganizationalObjectType`. [fg:symbols:extras.models.models:EventRule] [fg:symbols:extras.models.models:JournalEntry] [fg:symbols:extras.api.serializers_.events:EventRuleSerializer] [fg:symbols:extras.api.serializers_.journaling:JournalEntrySerializer] [fg:symbols:extras.forms.model_forms:WebhookForm] [fg:symbols:extras.forms.bulk_import:EventRuleImportForm] [fg:symbols:extras.filtersets:WebhookFilterSet] [fg:symbols:extras.graphql.types:JournalEntryType] [fg:symbols:extras.graphql.types:EventRuleType]

Every other change-logged model uses the lower tier: `ValidatedModelSerializer`, `forms.ModelForm`, `CSVModelForm`, `BulkEditForm`, `ChangeLoggedModelFilterSet`, plain `ObjectType`. [fg:symbols:extras.api.serializers_.customfields:CustomFieldSerializer] [fg:symbols:extras.forms.model_forms:CustomFieldForm] [fg:symbols:extras.forms.bulk_import:CustomFieldImportForm] [fg:symbols:extras.forms.bulk_edit:CustomLinkBulkEditForm] [fg:symbols:extras.filtersets:CustomFieldFilterSet] [fg:symbols:extras.graphql.types:CustomFieldType]

Models that are not change-logged (Script, Bookmark, TaggedItem, ObjectType) drop to `BaseFilterSet`/`django_filters.FilterSet`, and their tests compose subsets of `APIViewTestCases` instead of the full `APIViewTestCase`. [fg:symbols:extras.filtersets:ScriptFilterSet] [fg:symbols:extras.filtersets:BookmarkFilterSet] [fg:symbols:extras.filtersets:ObjectTypeFilterSet] [code:netbox/extras/tests/test_api.py:412-416] [code:netbox/extras/tests/test_api.py:547-549]

Exception: `JournalEntryBulkEditForm` is a plain `BulkEditForm` while `WebhookBulkEditForm` and `EventRuleBulkEditForm` are `NetBoxModelBulkEditForm`, so journal entries cannot be bulk-edited on custom fields or tags. [code:netbox/extras/forms/bulk_edit.py:376-386] [code:netbox/extras/forms/bulk_edit.py:233-236] [fg:symbols:extras.forms.bulk_edit:EventRuleBulkEditForm]

## 5. Full view family per model, registered with `@register_model_view`, URLs from `get_model_urls()`

Each model gets List/View/Edit(add+edit)/Delete/BulkImport/BulkEdit/BulkDelete classes in `views.py`, each decorated with `@register_model_view(Model, '<action>', path=..., detail=...)`, and `urls.py` contains only two `include(get_model_urls(...))` lines per model. [code:netbox/extras/views.py:45-100] [code:netbox/extras/views.py:434-477] [code:netbox/extras/urls.py:10-17]

Exceptions: Bookmark has only add/delete/bulk-delete; Notification exposes `read`/`dismiss` as plain `View`s and a delete view; ScriptModule has only edit/delete; script and dashboard-widget views are hand-listed in `urls.py`. [code:netbox/extras/views.py:403-427] [code:netbox/extras/views.py:495-534] [code:netbox/extras/views.py:1260-1273] [code:netbox/extras/urls.py:62-86]

## 6. Synced-data models implement `sync_data()` with `alters_data = True` and get a `bulk_sync` view

ExportTemplate, ConfigContext and ConfigTemplate inherit `SyncedDataMixin`, define `sync_data()` that copies from `data_file`, mark it `alters_data`, and are the three models with a `*BulkSyncDataView` and a `SyncedDataMixin` API viewset. [code:netbox/extras/models/models.py:430-435] [code:netbox/extras/models/configs.py:149-154] [code:netbox/extras/models/configs.py:234-239] [code:netbox/extras/views.py:280-282] [code:netbox/extras/views.py:925-927] [fg:symbols:extras.api.views:ExportTemplateViewSet] [fg:symbols:extras.api.views:ConfigContextViewSet]

The same `alters_data = True` marker is applied to `NotificationGroup.notify` and `populate_custom_field_defaults`, so templates cannot trigger side effects. [code:netbox/extras/models/notifications.py:176-184] [code:netbox/netbox/models/features.py:262-268]

## 7. User-scoped objects: owner FK plus `shared` flag, enforced in views, not models

SavedFilter and TableConfig carry `user` (SET_NULL) and `shared` fields; visibility is enforced by `SharedObjectViewMixin.get_queryset` (superuser sees all, anonymous sees shared, otherwise shared-or-own) mixed into all their views, and `alter_object` stamps the creating user. [code:netbox/extras/models/models.py:473-490] [code:netbox/extras/models/models.py:552-569] [code:netbox/extras/utils.py:21-34] [code:netbox/extras/views.py:289-334] [code:netbox/extras/views.py:344-393]

Strictly private per-user objects (Bookmark, Notification, Dashboard) instead override `get_queryset` to `filter(user=request.user)` or read `request.user.notifications`/`request.user.dashboard`, and cascade-delete with the user. [code:netbox/extras/views.py:403-427] [code:netbox/extras/views.py:495-534] [code:netbox/extras/models/models.py:818-821] [code:netbox/extras/models/dashboard.py:11-16] [code:netbox/extras/views.py:1185-1201]

## 8. Jinja2 everywhere user text becomes output, via `utilities.jinja2.render_jinja2`

Webhook payload URL, headers and body; CustomLink text and URL; and the shared `RenderTemplateMixin.render()` (ExportTemplate, ConfigTemplate) all go through `render_jinja2`; `RenderTemplateMixin` additionally passes `environment_params` and normalises CRLF. [code:netbox/extras/models/models.py:258-284] [code:netbox/extras/models/models.py:356-384] [code:netbox/extras/models/mixins.py:128-139]

CustomLink output is sanitised after rendering (`clean_html`, URL quoting, scheme allow-list from config); webhook and template output is not. [code:netbox/extras/models/models.py:368-378] [code:netbox/extras/webhooks.py:52-72]

## 9. Custom-field data lives in each object's JSONB and is repaired with server-side `jsonb_set`

`CustomField` never stores values; on add/remove/rename/delete, signal handlers call `populate_initial_data`, `remove_stale_data` and `rename_object_data`, which issue `UPDATE ... jsonb_set()`/key-deletion queries against every affected model table. [code:netbox/extras/models/customfields.py:281-328] [code:netbox/extras/signals.py:22-56] [code:netbox/extras/models/customfields.py:254-258]

Values cross the storage boundary through `serialize()`/`deserialize()`; the type switch is repeated in `to_form_field()` and `to_filter()`, and `CustomFieldChoiceSet.clean` queries `custom_field_data__<name>` to refuse removing in-use choices. [code:netbox/extras/models/customfields.py:408-446] [code:netbox/extras/models/customfields.py:594-652] [code:netbox/extras/models/customfields.py:845-869]

## 10. `q` search filters share one shape; ID and slug filter pairs for relations

Every filterset defines `q = CharFilter(method='search')` whose `search()` returns the unfiltered queryset on blank input and ORs `icontains` on name-like fields. [code:netbox/extras/filtersets.py:42-61] [code:netbox/extras/filtersets.py:83-90] [code:netbox/extras/filtersets.py:737-744] [code:netbox/extras/filtersets.py:807-813]

Relation filters come in `<rel>_id` (pk) and `<rel>` (slug, `to_field_name='slug'`) pairs, as throughout `ConfigContextFilterSet`. [code:netbox/extras/filtersets.py:593-625] [code:netbox/extras/filtersets.py:713-723]

Exception: `data_file_id` on both ConfigContextFilterSet and ConfigTemplateFilterSet is declared with `queryset=DataSource.objects.all()`, not DataFile. [code:netbox/extras/filtersets.py:728-731] [code:netbox/extras/filtersets.py:756-759]

## 11. Local imports to defer circular dependencies

Cross-package cycles (extras↔core, extras↔netbox, extras.events↔extras.jobs) are broken with function-local imports or `import_string`: `ScriptJob` inside `process_event_rules` and `ScriptView.post`; `Report`/`Script` inside `is_script`; `Dashboard` inside `get_default_dashboard`; `ConfigContext` inside `annotate_config_context_data`; `CustomField` inside four `CustomFieldsMixin` methods. [code:netbox/extras/events.py:126-138] [code:netbox/extras/views.py:1350-1361] [code:netbox/extras/utils.py:80-100] [code:netbox/extras/dashboard/utils.py:57-61] [code:netbox/extras/querysets.py:82-95] [code:netbox/netbox/models/features.py:202-204]

## 12. HTMX-aware views answer partials with `HX-Redirect` or status 286

Dashboard widget views refuse non-HTMX GETs, and on success reply with an `HX-Redirect` header; `NotificationDismissView` and `ScriptResultView` branch on `htmx_partial(request)`, the latter returning status 286 to stop polling once the job completes. [code:netbox/extras/views.py:1138-1140] [code:netbox/extras/views.py:1174-1176] [code:netbox/extras/views.py:522-527] [code:netbox/extras/views.py:1513-1521]

## 13. Package `__all__` plus star re-export

Every leaf module declares `__all__`, and package `__init__`s (`models`, `forms`, `api/serializers.py`) are pure `from .x import *` lists, so callers import `extras.models`/`extras.forms` and never a submodule. [code:netbox/extras/models/__init__.py:1-8] [code:netbox/extras/api/serializers.py:1-16] [code:netbox/extras/models/models.py:32-42] [code:netbox/extras/filtersets.py:19-39]

Exception: `models/mixins.py` deliberately omits `CustomStoragesLoader` from `__all__`, and `extras.querysets` is imported directly by dcim/virtualization. [code:netbox/extras/models/mixins.py:15-18] [fg:imports:dcim.models.devices->extras.querysets]
