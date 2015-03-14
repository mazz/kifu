"""Create routes here and gets returned into __init__ main()"""
from pyramid.wsgi import wsgiapp2

def build_routes(config):
    """Add any routes to the config"""

    # auth routes
    config.add_route("login", "/")
    config.add_route("logout", "logout")
    config.add_route("forgot_password", "forgot_password")
    config.add_route("reset", "{username}/reset/{reset_key}")
    config.add_route("signup", "signup")
    config.add_route("signup_process", "signup_process")
    config.add_route('list_users', '/list_users')

    config.add_route("user_account", "{username}/account")

    # ping checks
    config.add_route('api_ping',
                     '/api/v1/{username}/ping',
                     request_method='GET')
    config.add_route('api_ping_missing_user',
                     '/api/v1/ping',
                     request_method='GET')
    config.add_route('api_ping_missing_api',
                     '/ping',
                     request_method='GET')

    # auth related
    config.add_route("api_user_account",
                     "/api/v1/{username}/account",
                     request_method="GET")
    config.add_route("api_user_account_update",
                     "/api/v1/{username}/account",
                     request_method="POST")
    config.add_route("api_user_api_key",
                     "/api/v1/{username}/api_key")
    config.add_route("api_user_reset_password",
                     "/api/v1/{username}/password",
                     request_method="POST")

    config.add_route("api_user_suspend_remove",
                     "api/v1/suspend",
                     request_method="DELETE")
    config.add_route("api_user_suspend",
                     "api/v1/suspend",
                     request_method="POST")
    config.add_route("api_user_invite",
                     "api/v1/{username}/invite",
                     request_method="POST")

    # admin api calls
    # config.add_route("api_admin_readable_todo", "/api/v1/a/readable/todo")
    # config.add_route(
    #     "api_admin_readable_reindex",
    #     "/api/v1/a/readable/reindex")
    config.add_route(
        "api_admin_accounts_inactive",
        "/api/v1/a/accounts/inactive")
    config.add_route(
        "api_admin_accounts_invites_add",
        "/api/v1/a/accounts/invites/{username}/{count}",
        request_method="POST")
    config.add_route(
        "api_admin_accounts_invites",
        "/api/v1/a/accounts/invites",
        request_method="GET")
    # config.add_route(
    #     "api_admin_imports_list",
    #     "/api/v1/a/imports/list",
    #     request_method="GET")
    config.add_route(
        "api_admin_imports_reset",
        "/api/v1/a/imports/reset/{id}",
        request_method="POST")

    config.add_route(
        "api_admin_users_list",
        "/api/v1/a/users/list",
        request_method="GET")
    config.add_route(
        "api_admin_new_user",
        "/api/v1/a/users/add",
        request_method="POST")
    config.add_route(
        "api_admin_del_user",
        "/api/v1/a/users/delete/{username}",
        request_method="DELETE")
    # config.add_route(
    #     "api_admin_bmark_remove",
    #     "/api/v1/a/bmark/{username}/{hash_id}",
    #     request_method="DELETE")

    config.add_route(
        "api_admin_applog",
        "/api/v1/a/applog/list",
        request_method="GET")

    # these are single word matching, they must be after /recent /popular etc
    config.add_route("user_home", "{username}")

    return config
