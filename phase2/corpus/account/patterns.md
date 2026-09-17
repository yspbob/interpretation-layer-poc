# account — patterns and conventions (NetBox ea4c205)

## 1. Every tab view sets `active_tab`, and the base template keys on it

Each profile-area view renders with an `active_tab` value that `templates/account/base.html` compares against a fixed set (`profile`, `bookmarks`, `notifications`, `subscriptions`, `preferences`, `password`, `api-tokens`) to highlight the tab. Instances: `ProfileView` (`'profile'`), `UserConfigView` (`'preferences'`), `UserTokenListView` (`'api-tokens'`), and the three `ObjectListView` subclasses via `get_extra_context()` [code:netbox/account/views.py:199-202] [code:netbox/account/views.py:212-215] [code:netbox/account/views.py:287-290] [code:netbox/account/views.py:334-338] [code:netbox/templates/account/base.html:5-29].

Exceptions: `ChangePasswordView.get` sets `'password'` but its failed-POST re-render sets `'change_password'`, a value no tab checks, so the Password tab loses its highlight on a validation error; `UserTokenView` passes no `active_tab` at all [code:netbox/account/views.py:257-260] [code:netbox/account/views.py:270-273] [code:netbox/account/views.py:348-351] [code:netbox/templates/account/base.html:21-25].

## 2. Data is scoped to `request.user` in the view, not by permission filtering

Views that read data filter explicitly on the requesting user: `ProfileView` (`ObjectChange … filter(user=request.user)`), `UserTokenListView` (`UserToken.objects.filter(user=request.user)`), `UserTokenView` (`get_object_or_404(UserToken.objects.filter(user=request.user), pk=pk)`), `BookmarkListView` (`Bookmark.objects.filter(user=request.user)`), and the notification/subscription lists via the reverse relations `request.user.notifications` / `request.user.subscriptions` [code:netbox/account/views.py:194] [code:netbox/account/views.py:330] [code:netbox/account/views.py:345] [code:netbox/account/views.py:284-285] [code:netbox/account/views.py:301-302] [code:netbox/account/views.py:314-315].

Exception: `UserTokenEditView` and `UserTokenDeleteView` declare `queryset = UserToken.objects.all()` and rely on `ObjectPermissionRequiredMixin` to restrict the queryset by the caller's `ObjectPermission` constraints (defaulting to `{'user': '$user'}` from `DEFAULT_PERMISSIONS`); ownership on create is stamped in `alter_object()` [code:netbox/account/views.py:355-363] [code:netbox/account/views.py:367-369] [code:netbox/utilities/views.py:102-108] [code:netbox/netbox/settings.py:112-117].

## 3. Generic list views are reused by overriding `get_queryset()` and `get_extra_context()` only

The bookmark, notification and subscription tabs are `LoginRequiredMixin + generic.ObjectListView` subclasses that set `table` and `template_name`, override `get_queryset(request)` to the user's rows, and add `active_tab` through `get_extra_context()`; no filterset or actions are declared [code:netbox/account/views.py:280-290] [code:netbox/account/views.py:297-307] [code:netbox/account/views.py:310-320]. Because `ObjectListView.get_required_permission()` still demands `extras.view_<model>`, these views work for ordinary users only through the default self-constrained permissions [code:netbox/netbox/views/generic/bulk_views.py:64-65] [code:netbox/netbox/settings.py:97-111].

## 4. Forms and most tables are borrowed, not defined here

`account` defines no forms: `UserConfigView` uses `users.forms.UserConfigForm`, `UserTokenEditView` uses `users.forms.UserTokenForm`, and login/password use Django's `AuthenticationForm`/`PasswordChangeForm` [code:netbox/account/views.py:6] [code:netbox/account/views.py:210] [code:netbox/account/views.py:357]. Tables likewise come from `core` and `extras` (`ObjectChangeTable`, `BookmarkTable`, `NotificationTable`, `SubscriptionTable`); the single local table is `UserTokenTable` [code:netbox/account/views.py:23-25] [fg:symbols:account.tables:UserTokenTable].

Exception (indirection): `UserTokenListView` instantiates `tables.UserTokenTable` through the `users.tables` namespace rather than importing `account.tables` directly; that works only because `users.tables` imports the class at module level, even though it is not in `users.tables.__all__` [code:netbox/account/views.py:29] [code:netbox/account/views.py:331] [code:netbox/users/tables.py:4-13].

## 5. The language cookie is kept in step with the session

Three views manipulate `settings.LANGUAGE_COOKIE_NAME` with identical parameters (`max_age=request.session.get_expiry_age()`, `secure=settings.SESSION_COOKIE_SECURE`): `LoginView.post` sets it from `locale.language` in the user's config, `UserConfigView.post` sets or deletes it from the submitted form, and `LogoutView.get` deletes it together with `session_key` [code:netbox/account/views.py:128-135] [code:netbox/account/views.py:227-236] [code:netbox/account/views.py:176-179].

## 6. Redirect targets from the request are validated and log-sanitised

`LoginView.redirect_to_next()` accepts `next` only if `safe_for_redirect()` passes, otherwise logs a warning and falls back to `home`; the value is passed through `remove_linebreaks()` before logging, as is the failed-login username. The edit/delete token views inherit the same discipline from `GetReturnURLMixin.get_return_url()` for `return_url` [code:netbox/account/views.py:148-159] [code:netbox/account/views.py:140-141] [code:netbox/utilities/views.py:134-140].

Auth events use dedicated named loggers (`netbox.auth.login`, `netbox.auth.logout`) rather than the module logger [code:netbox/account/views.py:92] [code:netbox/account/views.py:103] [code:netbox/account/views.py:168].

## 7. Detail routes are registered, list/add routes are written by hand

`UserTokenView`, `UserTokenEditView` and `UserTokenDeleteView` are attached with `@register_model_view(UserToken, …)` and surfaced under `api-tokens/<int:pk>/` by `get_model_urls('account', 'usertoken')`, while `usertoken_list` and `usertoken_add` are explicit `path()` entries [code:netbox/account/views.py:341] [code:netbox/account/views.py:354] [code:netbox/account/views.py:366] [code:netbox/account/urls.py:16-18]. This differs from the `users` app, which registers its `add` and `list` token views through the decorator with `detail=False` [code:netbox/users/views.py:15] [code:netbox/users/views.py:28].

## 8. Token secrets are exposed only behind `ALLOW_TOKEN_RETRIEVAL`

The raw key reaches a template only when the setting is true: `UserTokenView` passes `key=None` otherwise, the table's copy button is wrapped in `{% if settings.ALLOW_TOKEN_RETRIEVAL %}`, and the concrete model's `__str__` falls back to a masked `partial` [code:netbox/account/views.py:346] [code:netbox/account/tables.py:15-19] [code:netbox/users/models/tokens.py:78-86].

## 9. User feedback via `django.contrib.messages` after every state change

Login, logout, preference save, password change and the LDAP refusal each emit a translated message before redirecting [code:netbox/account/views.py:118] [code:netbox/account/views.py:174] [code:netbox/account/views.py:224] [code:netbox/account/views.py:252] [code:netbox/account/views.py:267].

Minor inconsistency: `views.py` aliases `gettext_lazy as _` while `tables.py` aliases `gettext as _`; and `LoginView.get` passes `login_form_hidden` to the template but the failed-POST re-render does not [code:netbox/account/views.py:16] [code:netbox/account/tables.py:1] [code:netbox/account/views.py:96-100] [code:netbox/account/views.py:143-146].
