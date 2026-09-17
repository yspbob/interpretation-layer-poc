# users — patterns and conventions

## Package layout: one file per concern, star re-exported through a facade

Models, forms and API serializers are each split into a package whose `__init__.py` (or `serializers.py`) does nothing but `from .x import *`, and every leaf module declares `__all__` so the star import is bounded [code:netbox/users/models/__init__.py:1-4] [code:netbox/users/forms/__init__.py:1-4] [code:netbox/users/api/serializers.py:1-3] [code:netbox/users/models/tokens.py:16-18] [code:netbox/users/forms/bulk_edit.py:12-17]. Consumers inside the app therefore import from the facade (`from users.models import *`, `from . import serializers`), not from the leaf [code:netbox/users/forms/model_forms.py:14] [code:netbox/users/api/views.py:18].

## Views are declared, not routed

Every UI view is a `netbox.views.generic` subclass decorated with `@register_model_view(Model, action, path=..., detail=...)`, and `urls.py` only calls `get_model_urls('users', <model>)` twice per model (list-level and detail-level) [code:netbox/users/views.py:15-31] [code:netbox/users/views.py:64-75] [code:netbox/users/urls.py:9-19]. The standard set per model is list, detail, add/edit (one class with two decorators), delete, bulk_import, bulk_edit, bulk_delete [code:netbox/users/views.py:125-170]. **Exception:** `ObjectPermission` has no bulk-import view and no import form, and its view test case correspondingly omits `BulkImportObjectsViewTestCase` [code:netbox/users/views.py:176-214] [code:netbox/users/forms/bulk_import.py:7-11] [code:netbox/users/tests/test_views.py:157-165].

## Every public model uses `RestrictedQuerySet` as its manager

`Token` and `ObjectPermission` set `objects = RestrictedQuerySet.as_manager()`; `User` and `Group` wrap Django's stock managers with `.from_queryset(RestrictedQuerySet)` so `create_user`/`create_superuser` survive [code:netbox/users/models/tokens.py:72] [code:netbox/users/models/permissions.py:46] [code:netbox/users/models/users.py:22-23] [code:netbox/users/models/users.py:70-71]. The API `UserViewSet` even builds its queryset as `RestrictedQuerySet(model=User)` explicitly [code:netbox/users/api/views.py:33-36]. **Exception:** `UserConfig` has no custom manager and is flagged `_netbox_private = True`, keeping it out of the public model registry [code:netbox/users/models/preferences.py:12-25] [code:netbox/netbox/models/features.py:655-658].

## Models are plain Django models, not `NetBoxModel`

All four public models subclass `models.Model` or `AbstractUser` directly and carry only `ordering`, `verbose_name`, `__str__`, `get_absolute_url` (reversing a `users:<model>` route) [code:netbox/users/models/users.py:26-64] [code:netbox/users/models/permissions.py:13-54] [code:netbox/users/models/tokens.py:21-72]. Cross-model relations are string references (`to='users.User'`, `to='core.ObjectType'`), never imported classes [fg:model_refs:users.models.tokens:26] [fg:model_refs:users.models.preferences:16] [fg:model_refs:users.models.permissions:31].

## Bulk-edit forms are hand-rolled `forms.Form` with the BulkEditForm attribute contract

`UserBulkEditForm`, `GroupBulkEditForm` and `ObjectPermissionBulkEditForm` subclass `forms.Form` yet declare the attributes the generic view expects: a hidden `pk` `ModelMultipleChoiceField`, `model`, `fieldsets`, `nullable_fields`, and `BulkEditNullBooleanSelect` for booleans [code:netbox/users/forms/bulk_edit.py:20-55] [code:netbox/users/forms/bulk_edit.py:76-96]. **Exceptions:** `TokenBulkEditForm` subclasses `utilities.forms.BulkEditForm` instead [code:netbox/users/forms/bulk_edit.py:99-131]; and `GroupBulkEditForm` sets `model = User`, not `Group` [code:netbox/users/forms/bulk_edit.py:58-69].

## Filter forms use `NetBoxModelFilterSetForm` with a `q`/`filter_id` first fieldset

`GroupFilterForm`, `UserFilterForm` and `ObjectPermissionFilterForm` all begin with `FieldSet('q', 'filter_id')` and use `BOOLEAN_WITH_BLANK_CHOICES` selects for tri-state booleans [code:netbox/users/forms/filtersets.py:20-45] [code:netbox/users/forms/filtersets.py:62-75]. **Exception:** `TokenFilterForm` composes `SavedFiltersMixin` with the plain `FilterForm` [code:netbox/users/forms/filtersets.py:116-121].

## Filtersets pair an `_id` filter with a natural-key filter

Related objects are filterable both by PK and by name: `user_id`/`user` (`to_field_name='username'`) on Token and ObjectPermission, `group_id`/`group` (`to_field_name='name'`) on User and ObjectPermission [code:netbox/users/filtersets.py:104-114] [code:netbox/users/filtersets.py:59-69] [code:netbox/users/filtersets.py:171-192]. All four filtersets implement `q` as a `CharFilter(method='search')` that returns the queryset unchanged on blank input and ORs `icontains` across text fields [code:netbox/users/filtersets.py:45-51] [code:netbox/users/filtersets.py:138-144]. `GroupFilterSet` and `UserFilterSet` alone lack the natural-key counterpart for `permission_id` and `notification_group_id` [code:netbox/users/filtersets.py:25-39] [code:netbox/users/filtersets.py:70-79].

## Passwords only ever pass through `set_password`

Nowhere is `password` assigned as a model field value: `UserForm.save`, `UserImportForm.save`, `UserSerializer.create` and `UserSerializer.update` all pop the plaintext and call `instance.set_password()` [code:netbox/users/forms/model_forms.py:214-222] [code:netbox/users/forms/bulk_import.py:30-34] [code:netbox/users/api/serializers_/users.py:70-89]. Django's `password_validation.validate_password` is invoked in both the form `clean` and the serializer `validate` [code:netbox/users/forms/model_forms.py:230-232] [code:netbox/users/api/serializers_/users.py:62-68]. Both the API and view test cases set `validation_excluded_fields = ['password']` [code:netbox/users/tests/test_api.py:19-22] [code:netbox/users/tests/test_views.py:6-19].

## `ALLOW_TOKEN_RETRIEVAL` is checked at every layer that could show a key

`Token.__str__` returns the masked `partial` unless the setting is on; `TokenSerializer.key` is `write_only=not settings.ALLOW_TOKEN_RETRIEVAL`; `UserTokenForm.__init__` deletes the `key` field on existing tokens when it is off [code:netbox/users/models/tokens.py:78-86] [code:netbox/users/api/serializers_/tokens.py:17-23] [code:netbox/users/forms/model_forms.py:141-146]. Key generation is likewise triplicated so a key exists whichever path creates the token: `Token.save`, `TokenSerializer.to_internal_value`, and the form's `initial['key']` [code:netbox/users/models/tokens.py:88-96] [code:netbox/users/api/serializers_/tokens.py:41-44] [code:netbox/users/forms/model_forms.py:148-150].

## M2M relations are exposed through `SerializedPKRelatedField(nested=True)` and reverse M2Ms via manual `.set()`

Serializers accept PKs and emit brief nested objects for `groups`/`permissions`/`users`, and every serializer declares `brief_fields` [code:netbox/users/api/serializers_/users.py:17-31] [code:netbox/users/api/serializers_/permissions.py:12-29]. The `permissions` API field is aliased from the model's `object_permissions` via `source=` [code:netbox/users/api/serializers_/users.py:19-26] [code:netbox/users/api/serializers_/users.py:42-49]. On the form side, reverse relations (`GroupForm.users`, `ObjectPermissionForm.users/groups`) are `DynamicModelMultipleChoiceField`s whose `initial` is loaded from `values_list('id')` in `__init__` and written back with `.set()` in `save` [code:netbox/users/forms/model_forms.py:259-272] [code:netbox/users/forms/model_forms.py:338-341] [code:netbox/users/forms/model_forms.py:386-393].

## The `display` of a User is "username (Full Name)" in every serializer

`UserSerializer.get_display` and `NestedUserSerializer.get_display` implement the same walrus expression [code:netbox/users/api/serializers_/users.py:91-95] [code:netbox/users/api/serializers_/nested.py:26-30].

## Tables: linkified name, explicit `ActionsColumn(('edit','delete'))`

`UserTable`, `GroupTable` and `ObjectPermissionTable` all linkify their name column and restrict row actions to edit/delete; M2M columns use `linkify_item` to `users:group`/`users:user` [code:netbox/users/tables.py:29-49] [code:netbox/users/tables.py:60-67] [code:netbox/users/tables.py:101-111]. **Exception:** `TokenTable` inherits from `account.tables.UserTokenTable` rather than `NetBoxTable` [code:netbox/users/tables.py:16-26].

## GraphQL types are the same shape everywhere

Each `strawberry_django.type` lists explicit `fields`, points at a `filter_type` built on `BaseObjectTypeFilterMixin`, and enables pagination; `UsersQuery` exposes `<model>` and `<model>_list` per type [code:netbox/users/graphql/types.py:15-34] [code:netbox/users/graphql/filters.py:17-30] [code:netbox/users/graphql/schema.py:9-15].

## Data migrations use `apps.get_model` and a no-op reverse

Migrations 0005, 0006 and 0009 each define a module-level function that fetches historical models via `apps.get_model('extras', 'CustomField')` etc., scope queries with `using(db_alias)`, and are wired with `reverse_code=migrations.RunPython.noop` [code:netbox/users/migrations/0005_alter_user_table.py:4-18] [code:netbox/users/migrations/0006_custom_group_model.py:5-16] [code:netbox/users/migrations/0009_update_group_perms.py:4-16] [fg:model_refs:users.migrations.0005_alter_user_table:6] [fg:model_refs:users.migrations.0009_update_group_perms:5]. Table, sequence, index and constraint renames are raw `RunSQL` [code:netbox/users/migrations/0005_alter_user_table.py:40-49] [code:netbox/users/migrations/0008_flip_objectpermission_assignments.py:23-31].

## Translation: models and forms use `gettext_lazy`; filtersets, tables and bulk_import use `gettext`

Model `verbose_name`s and form labels are wrapped in `gettext_lazy as _` [code:netbox/users/models/users.py:10] [code:netbox/users/forms/model_forms.py:7]. **Exception:** `filtersets.py`, `tables.py` and `forms/bulk_import.py` import the eager `gettext as _` for labels evaluated at class-definition time [code:netbox/users/filtersets.py:4] [code:netbox/users/tables.py:2] [code:netbox/users/forms/bulk_import.py:2].
