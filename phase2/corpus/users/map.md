# users — subsystem map (NetBox @ ea4c205)

## What it is

`users` is the Django app that owns NetBox's identity and authorization data: the swapped-in `User` model, a custom `Group`, the `ObjectPermission` model that drives NetBox's object-level permission backend, per-user API `Token`s, and the `UserConfig` JSON preference store. It is 40 non-test modules and 3,520 lines of code, with 6 test modules [fg:subsystems:users]. Django is pointed at it by `AUTH_USER_MODEL = 'users.User'` in project settings, so every `settings.AUTH_USER_MODEL` reference in the codebase resolves here [code:netbox/netbox/settings.py:521].

## Modules by role

**Models** live in a package with four files re-exported by `models/__init__.py` via star imports [code:netbox/users/models/__init__.py:1-4].
- `models/users.py`: `Group` (plain `models.Model` with a `permissions` M2M to `auth.Permission` kept "for authentication backend compatibility"), `User` (subclass of `AbstractUser` whose `groups` M2M is redirected to `users.Group`), and two managers built from `RestrictedQuerySet` [code:netbox/users/models/users.py:22-53] [code:netbox/users/models/users.py:70-88] [fg:model_refs:users.models.users:75].
- `models/permissions.py`: `ObjectPermission` with `actions` as a Postgres `ArrayField`, `constraints` as JSON, and `object_types` M2M to `core.ObjectType` [code:netbox/users/models/permissions.py:13-46] [fg:model_refs:users.models.permissions:31].
- `models/tokens.py`: `Token` with FK to `users.User`, a 40-char unique key auto-generated on save, expiry, `write_enabled`, and `allowed_ips` as an array of `ipam.fields.IPNetworkField` [code:netbox/users/models/tokens.py:21-72] [code:netbox/users/models/tokens.py:88-96] [fg:model_refs:users.models.tokens:26].
- `models/preferences.py`: `UserConfig`, a one-to-one JSON blob per user with dotted-path `get`/`set`/`clear`, marked `_netbox_private = True` [code:netbox/users/models/preferences.py:12-25] [fg:model_refs:users.models.preferences:16].

None of these inherit `NetBoxModel`; they are plain Django models, so they get no change logging, custom fields, tags or journaling from the `netbox.models` feature mixins [code:netbox/users/models/users.py:26] [code:netbox/users/models/permissions.py:13] [code:netbox/users/models/tokens.py:21].

**Views** (`views.py`, 27 classes) are the standard NetBox generic CRUD set for Token, User, Group and ObjectPermission, each registered with `@register_model_view` [code:netbox/users/views.py:15-57] [fg:modules:users.views]. `urls.py` contains no explicit routes; it delegates entirely to `get_model_urls` per model [code:netbox/users/urls.py:9-19] [fg:entrypoints:users.urls].

**Forms** are a package of four modules star-exported from `forms/__init__.py` [code:netbox/users/forms/__init__.py:1-4]: `model_forms.py` (UserConfigForm with a metaclass that synthesizes one field per registered preference, UserTokenForm/TokenForm, UserForm, GroupForm, ObjectPermissionForm) [code:netbox/users/forms/model_forms.py:32-58] [fg:modules:users.forms.model_forms]; `bulk_edit.py`, `bulk_import.py`, `filtersets.py` [fg:modules:users.forms.bulk_edit] [fg:modules:users.forms.bulk_import] [fg:modules:users.forms.filtersets].

**Filtersets** (`filtersets.py`) define one `BaseFilterSet` per model; all four provide a `q` search method, and ObjectPermissionFilterSet adds `can_view`/`can_add`/`can_change`/`can_delete` boolean filters that query the `actions` array [code:netbox/users/filtersets.py:147-170] [code:netbox/users/filtersets.py:206-211].

**Tables** (`tables.py`): `UserTable`, `GroupTable`, `ObjectPermissionTable` extend `NetBoxTable`; `TokenTable` instead extends `account.tables.UserTokenTable` and adds a `user` column [code:netbox/users/tables.py:16-27] [fg:imports:users.tables->account.tables].

**REST API** (`api/`): `serializers.py` is a facade that star-imports `serializers_/{users,permissions,tokens}.py` [code:netbox/users/api/serializers.py:1-3]. `api/views.py` holds four `NetBoxModelViewSet`s plus two non-model endpoints: `TokenProvisionView` (unauthenticated `APIView`, `permission_classes = []`) and `UserConfigViewSet` (a bare `ViewSet` that only exposes the requesting user's own config) [code:netbox/users/api/views.py:55-59] [code:netbox/users/api/views.py:95-102]. `api/urls.py` registers the router under app name `users-api` and adds `tokens/provision/` [code:netbox/users/api/urls.py:8-26] [fg:entrypoints:users.api.urls].

**GraphQL** (`graphql/`): only `Group` and `User` are exposed (`GroupType`, `UserType`, `UsersQuery`); Token, ObjectPermission and UserConfig have no GraphQL surface, which the API tests note explicitly ("No GraphQL support for Token") [code:netbox/users/graphql/schema.py:9-15] [code:netbox/users/tests/test_api.py:191-198].

**Signals** (`signals.py`): a `post_save` receiver on `User` creates a `UserConfig` seeded from `DEFAULT_USER_PREFERENCES`, and a `user_login_failed` receiver logs failed logins with client IP [code:netbox/users/signals.py:12-32] [fg:entrypoints:users.signals]. Signals are wired in `UsersConfig.ready()`, which also calls `register_models` on every model in the app [code:netbox/users/apps.py:4-12].

**Support modules**: `constants.py` defines `OBJECTPERMISSION_OBJECT_TYPES` (the Q that limits which content types a permission may target) and `CONSTRAINT_TOKEN_USER = '$user'` [code:netbox/users/constants.py:4-9]; `preferences.py` defines the `UserPreference` descriptor class consumed by `netbox.preferences.PREFERENCES` [code:netbox/users/preferences.py:1-11] [fg:imports:netbox.preferences->users.preferences]; `utils.py` has `clean_username` built on social-core regexes [code:netbox/users/utils.py:1-9].

**Tests**: `test_api.py` (427 loc), `test_filtersets.py`, `test_views.py`, `test_models.py` (UserConfig get/set/clear), `test_preferences.py` [fg:modules:users.tests.test_api] [fg:modules:users.tests.test_models] [fg:modules:users.tests.test_preferences].

**Migrations**: two squashed migrations cover history through NetBox 3.x; 0005–0009 are the 4.0 transition that moved User off `auth_user`, replaced `auth.Group` with `users.Group`, repointed `object_types` at `core.ObjectType`, and flipped the ObjectPermission M2M ownership [fg:modules:users.migrations.0001_squashed_0011] [fg:modules:users.migrations.0005_alter_user_table] [fg:modules:users.migrations.0006_custom_group_model] [fg:modules:users.migrations.0008_flip_objectpermission_assignments].

## Dependencies (outbound)

Outbound edges go mostly to `utilities` (28) and `netbox` (19), then `core` (9), `ipam` (6), `dcim` (2, tests only), `extras` (1) and `account` (1); the notable ones are listed below [fg:subsystems:users].
- `core.models.ObjectType` is the target of `ObjectPermission.object_types` and is used by the permission form, filterset and serializer [fg:model_refs:users.models.permissions:31] [fg:imports:users.forms.model_forms->core.models] [fg:imports:users.api.serializers_.permissions->core.models].
- `ipam.fields.IPNetworkField` and `ipam.formfields`/`ipam.validators` back `Token.allowed_ips` at the model, form and bulk-edit layers [fg:imports:users.models.tokens->ipam.fields] [fg:imports:users.forms.model_forms->ipam.formfields] [fg:imports:users.forms.bulk_edit->ipam.validators].
- `extras.models.NotificationGroup` is imported by `filtersets.py` for `notification_group_id` filters on Group and User [code:netbox/users/filtersets.py:35-39] [fg:imports:users.filtersets->extras.models].
- `account.tables.UserTokenTable` is the base of `TokenTable`, a reverse dependency on an app that itself depends on `users` [fg:imports:users.tables->account.tables] [fg:imports:account.models->users.models].
- `netbox.config.get_config` supplies `DEFAULT_USER_PREFERENCES` to both the signal and `UserConfig.get` [fg:imports:users.signals->netbox.config] [fg:imports:users.models.preferences->netbox.config].
- `utilities.permissions.qs_filter_from_constraints` is used by `ObjectPermissionForm.clean` to validate constraints by running a query [code:netbox/users/forms/model_forms.py:367-384] [fg:imports:users.forms.model_forms->utilities.permissions].

## Dependents (inbound)

Inbound edges come from `extras` (17), `dcim` (10), `netbox` (10), `core` (9), `utilities` (6), `account` (3), `circuits` (1), `ipam` (1); the load-bearing ones are listed below [fg:subsystems:users].
- The authentication backend `netbox.authentication.ObjectPermissionMixin` queries `ObjectPermission` filtered by `Q(users=user_obj) | Q(groups__user=user_obj)` and expands `object_types × actions` into permission names [code:netbox/netbox/authentication/__init__.py:75-107] [fg:imports:netbox.authentication->users.models]. Remote-auth also creates `ObjectPermission` rows directly [code:netbox/netbox/authentication/__init__.py:285-294].
- `netbox.api.authentication.TokenAuthentication` uses `Token` as its model and enforces `allowed_ips`, `last_used` throttling and `is_expired` [code:netbox/netbox/api/authentication.py:13-59] [fg:imports:netbox.api.authentication->users.models].
- `utilities.querysets.RestrictedQuerySet.restrict` and `utilities.permissions.qs_filter_from_constraints` import `CONSTRAINT_TOKEN_USER` from `users.constants`; the latter resolves `users.User` via `apps.get_model` to avoid a circular import [code:netbox/utilities/permissions.py:85-99] [fg:imports:utilities.querysets->users.constants] [fg:model_refs:utilities.permissions:96].
- `account` is a thin veneer: `account.models.UserToken` is a proxy of `Token` marked `_netbox_private`, and `account.views` reuses `users.forms.UserConfigForm` and `UserTokenForm` [code:netbox/account/models.py:6-17] [code:netbox/account/views.py:29-30] [fg:imports:account.views->users].
- `UserSerializer` is imported by `core`, `dcim` and `extras` serializers for nested user fields (change logs, jobs, racks, bookmarks, notifications) [fg:imports:core.api.serializers_.change_logging->users.api.serializers_.users] [fg:imports:dcim.api.serializers_.racks->users.api.serializers_.users] [fg:imports:extras.api.serializers_.bookmarks->users.api.serializers_.users].
- String-reference inbound: `extras.Dashboard.user` (OneToOne), `extras.NotificationGroup.groups/users` (M2M) [fg:model_refs:extras.models.dashboard:12] [fg:model_refs:extras.models.notifications:135] [fg:model_refs:extras.models.notifications:141].
- `netbox.graphql.schema` merges `UsersQuery` into the root schema; `dcim`/`extras` GraphQL types and filters import `users.graphql.types`/`filters` [fg:imports:netbox.graphql.schema->users.graphql.schema] [fg:imports:dcim.graphql.types->users.graphql.types] [fg:imports:extras.graphql.filters->users.graphql.filters].
- `utilities.testing.*` imports `users.models` for `create_test_user` and permission helpers, so every test in the codebase depends on this app [fg:imports:utilities.testing.base->users.models] [fg:imports:utilities.testing.api->users.models].

Settings also list all four public models in `EXEMPT_EXCLUDE_MODELS`, so they can never be exempted from view permission by wildcard [code:netbox/netbox/settings.py:571-578].

## Entry points

- UI: `netbox/urls.py` mounts `users.urls` at `/users/` [code:netbox/netbox/urls.py:32] [fg:entrypoints:users.urls].
- REST: `netbox/urls.py` mounts `users.api.urls` at `/api/users/` [code:netbox/netbox/urls.py:51] [fg:entrypoints:users.api.urls].
- Signals: `users.signals` loaded from `UsersConfig.ready()` [code:netbox/users/apps.py:7-9] [fg:entrypoints:users.signals].
- GraphQL: `UsersQuery` composed into the root `Query` [code:netbox/netbox/graphql/schema.py:14-22].

## Where change concentrates

`views.py` is by far the most-touched module (88 commits, 9 authors, 2016–2025) followed by `api/serializers.py` (40) and `tests/test_api.py` (35) [fg:churn:users.views] [fg:churn:users.api.serializers] [fg:churn:users.tests.test_api]. `forms/model_forms.py` is the most recently active (30 commits, last 2025-06-26) [fg:churn:users.forms.model_forms]. The models themselves have almost no history at their current paths because the `models/` package was created in April 2024 (1–2 commits each) [fg:churn:users.models.users] [fg:churn:users.models.permissions]. The 4.0 migrations 0005 and 0006 were each revised 7 times through May 2025, indicating the User/Group table moves needed repeated fixes [fg:churn:users.migrations.0005_alter_user_table] [fg:churn:users.migrations.0006_custom_group_model].
