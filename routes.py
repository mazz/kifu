"""Create routes here and gets returned into __init__ main()"""
from pyramid.wsgi import wsgiapp2

def build_routes(config):
    """Add any routes to the config"""

    config.add_route("signup_process", "/")
    # auth routes
    config.add_route("login", "login")
    config.add_route("logout", "logout")
    config.add_route("reset", "{username}/reset/{reset_key}")
    config.add_route("signup", "signup")
    #config.add_route("signup_process", "signup_process")
    config.add_route('list_users', '/list_users')

    config.add_route("user_account", "{username}/account")

    return config
