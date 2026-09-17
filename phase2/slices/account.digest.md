# Fact-graph digest: subsystem `account` at T0 ea4c205

Summary row [fg:subsystems:account]: {'subsystem': 'account', 'modules': 6, 'loc_code': 469, 'loc_data': 0, 'test_modules': 0}

## Modules (id = modules:<module>) — module | path | loc | classes | functions | test | migration
- account | netbox/account/__init__.py | 1 | 0 | 0 |  | 
- account.migrations | netbox/account/migrations/__init__.py | 1 | 0 | 0 |  | 
- account.migrations.0001_initial | netbox/account/migrations/0001_initial.py | 28 | 1 | 0 |  | migration
- account.models | netbox/account/models.py | 18 | 1 | 0 |  | 
- account.tables | netbox/account/tables.py | 58 | 1 | 0 |  | 
- account.urls | netbox/account/urls.py | 21 | 0 | 0 |  | 
- account.views | netbox/account/views.py | 370 | 12 | 0 |  | 

## Import edges (id = imports:<src>-><dst>; full rows in the slice file)
Outbound by target subsystem: {'netbox': 4, 'utilities': 4, 'users': 3, 'account': 3, 'core': 2, 'extras': 2}
Inbound by source subsystem: {'netbox': 1, 'users': 1}

## Outbound imports to OTHER subsystems (src -> dst)
- account.models -> users.models [fg:imports:account.models->users.models]
- account.tables -> netbox.tables [fg:imports:account.tables->netbox.tables]
- account.urls -> utilities.urls [fg:imports:account.urls->utilities.urls]
- account.views -> core.models [fg:imports:account.views->core.models]
- account.views -> core.tables [fg:imports:account.views->core.tables]
- account.views -> extras.models [fg:imports:account.views->extras.models]
- account.views -> extras.tables [fg:imports:account.views->extras.tables]
- account.views -> netbox.authentication [fg:imports:account.views->netbox.authentication]
- account.views -> netbox.config [fg:imports:account.views->netbox.config]
- account.views -> netbox.views [fg:imports:account.views->netbox.views]
- account.views -> users [fg:imports:account.views->users]
- account.views -> users.models [fg:imports:account.views->users.models]
- account.views -> utilities.request [fg:imports:account.views->utilities.request]
- account.views -> utilities.string [fg:imports:account.views->utilities.string]
- account.views -> utilities.views [fg:imports:account.views->utilities.views]

## Inbound imports from OTHER subsystems (src -> dst)
- netbox.urls -> account.views [fg:imports:netbox.urls->account.views]
- users.tables -> account.tables [fg:imports:users.tables->account.tables]

## String references (id = model_refs:<module>:<lineno>) — module | class.field | kind | target | cross_app

## String references INTO this subsystem from others

## Churn (id = churn:<module>)
- account.views | 22 commits | 5 authors | 2023-07-31 .. 2025-06-03 [fg:churn:account.views]
- account.migrations.0001_initial | 2 commits | 2 authors | 2023-07-31 .. 2025-03-07 [fg:churn:account.migrations.0001_initial]
- account.models | 2 commits | 1 authors | 2023-07-31 .. 2023-11-03 [fg:churn:account.models]
- account.tables | 2 commits | 1 authors | 2023-07-31 .. 2024-04-17 [fg:churn:account.tables]
- account.urls | 2 commits | 1 authors | 2023-07-31 .. 2024-07-15 [fg:churn:account.urls]
- account | 1 commits | 1 authors | 2023-07-31 .. 2023-07-31 [fg:churn:account]
- account.migrations | 1 commits | 1 authors | 2023-07-31 .. 2023-07-31 [fg:churn:account.migrations]

## Entry points (id = entrypoints:<module>)
- urls | account.urls | netbox/account/urls.py [fg:entrypoints:account.urls]

## Symbols: classes per module (id = symbols:<module>:<name>)
- account.migrations.0001_initial: Migration
- account.models: UserToken
- account.tables: UserTokenTable
- account.views: LoginView, LogoutView, ProfileView, UserConfigView, ChangePasswordView, BookmarkListView, NotificationListView, SubscriptionListView, UserTokenListView, UserTokenView, UserTokenEditView, UserTokenDeleteView
