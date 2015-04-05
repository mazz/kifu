"""Controllers related to viewing lists of bookmarks"""
import logging

from datetime import datetime
from pyramid.settings import asbool
from pyramid.view import view_config
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import contains_eager
from StringIO import StringIO

from ~~~PROJNAME~~~.queue import tasks
from ~~~PROJNAME~~~.lib.access import api_auth
from ~~~PROJNAME~~~.lib.applog import AuthLog
from ~~~PROJNAME~~~.lib.msg import ReactivateMsg
from ~~~PROJNAME~~~.lib.msg import InvitationMsg
#from ~~~PROJNAME~~~.lib.readable import ReadContent
#from ~~~PROJNAME~~~.lib.tagcommands import Commander

#from ~~~PROJNAME~~~.models import Bmark
#from ~~~PROJNAME~~~.models import BmarkMgr
from ~~~PROJNAME~~~.models import DBSession
from ~~~PROJNAME~~~.models import NoResultFound
#from ~~~PROJNAME~~~.models import Readable
#from ~~~PROJNAME~~~.models import TagMgr
from ~~~PROJNAME~~~.models.applog import AppLogMgr
from ~~~PROJNAME~~~.models.auth import ActivationMgr
from ~~~PROJNAME~~~.models.auth import get_random_word
from ~~~PROJNAME~~~.models.auth import User
from ~~~PROJNAME~~~.models.auth import UserMgr
#from ~~~PROJNAME~~~.models.queue import ImportQueueMgr

#from ~~~PROJNAME~~~.models.fulltext import get_fulltext_handler

LOG = logging.getLogger(__name__)
RESULTS_MAX = 10
HARD_MAX = 100


def _check_with_content(params):
    """Verify that we should be checking with content"""
    if 'with_content' in params and params['with_content'] != 'false':
        return True
    else:
        return False


def _api_response(request, data):
    """Perform common operations on the response."""
    # Wrap the data response with CORS headers for cross domain JS clients.
    request.response.headers.extend([
        ('Access-Control-Allow-Origin', '*'),
        ('Access-Control-Allow-Headers', 'X-Requested-With')
    ])

    return data


@view_config(route_name="api_ping", renderer="jsonp")
@api_auth('api_key', UserMgr.get)
def ping(request):
    """Verify that you've setup your api correctly and verified

    """
    return _api_response(request, {
        'success': True,
        'message': 'Looks good'
    })


@view_config(route_name="api_ping_missing_user", renderer="jsonp")
def ping_missing_user(request):
    """You ping'd but were missing the username in the url for some reason.

    """
    return _api_response(request, {
        'success': False,
        'message': 'Missing username in your api url.'
    })


@view_config(route_name="api_ping_missing_api", renderer="jsonp")
def ping_missing_api(request):
    """You ping'd but didn't specify the actual api url.

    """
    return _api_response(request, {
        'success': False,
        'message': 'The API url should be /api/v1'
    })


# USER ACCOUNT INFORMATION CALLS
@view_config(route_name="api_user_account", renderer="jsonp")
@api_auth('api_key', UserMgr.get)
def account_info(request):
    """Return the details of the user account specifed

    expecting username in matchdict
    We only return a subset of data. We're not sharing keys such as api_key,
    password hash, etc.

    """
    user = request.user

    return _api_response(request, user.safe_data())


@view_config(route_name="api_user_account_update", renderer="jsonp")
@api_auth('api_key', UserMgr.get)
def account_update(request):
    """Update the account information for a user

    :params name:
    :params email:

    Callable by either a logged in user or the api key for mobile apps/etc

    """
    params = request.params
    json_body = request.json_body
    user_acct = request.user

    if 'name' in params and params['name'] is not None:
        name = params.get('name')
        user_acct.name = name

    if 'name' in json_body and json_body['name'] is not None:
        name = json_body.get('name')
        user_acct.name = name

    if 'email' in params and params['email'] is not None:
        email = params.get('email')
        user_acct.email = email

    if 'email' in json_body and json_body['email'] is not None:
        email = json_body.get('email')
        user_acct.email = email

    return _api_response(request, user_acct.safe_data())


@view_config(route_name="api_user_api_key", renderer="jsonp")
@api_auth('api_key', UserMgr.get)
def api_key(request):
    """Return the currently logged in user's api key

    This api call is available both on the website via a currently logged in
    user and via a valid api key passed into the request. In this way we should
    be able to add this to the mobile view with an ajax call as well as we do
    into the account information on the main site.

    """
    user_acct = request.user
    return _api_response(request, {
        'api_key': user_acct.api_key,
        'username': user_acct.username
    })


@view_config(route_name="api_user_reset_password", renderer="jsonp")
@api_auth('api_key', UserMgr.get)
def reset_password(request):
    """Change a user's password from the current string

    :params current_password:
    :params new_password:

    Callable by either a logged in user or the api key for mobile apps/etc

    """

    params = request.params

    # now also load the password info
    current = params.get('current_password', None)
    new = params.get('new_password', None)

    # if we don't have any password info, try a json_body in case it's a json
    #POST
    if current is None and new is None:
        params = request.json_body
        current = params.get('current_password', None)
        new = params.get('new_password', None)

    user_acct = request.user

    LOG.error("PASSWD")
    LOG.error(current)
    LOG.error(new)
    if not UserMgr.acceptable_password(new):
        request.response.status_int = 406
        return _api_response(request, {
            'username': user_acct.username,
            'error': "Come on, let's try a real password this time"
        })

    # before we change the password, let's verify it
    if user_acct.validate_password(current):
        # we're good to change it
        user_acct.password = new
        return _api_response(request, {
            'username': user_acct.username,
            'message': "Password changed",
        })
    else:
        request.response.status_int = 403
        return _api_response(request, {
            'username': user_acct.username,
            'error': "There was a typo somewhere. Please check your request"
        })


@view_config(route_name="api_user_username_exists", renderer="jsonp")
def username_exists(request):
    params = request.params

    # import pdb; pdb.set_trace()

    # now also load the password info
    username = params.get('username', None)

    if username is None and hasattr(request, 'json_body'):
        # try the json body
        username = request.json_body.get('username', None)

    if username is None:
        request.response.status_int = 406
        return _api_response(request, {
            'error': "Please submit a username",
        })

    user = UserMgr.get(username=username)

    response_dict = {}
    if user is None:
        response_dict = {
            'exists': False,
            }
    else:
        response_dict = {
            'exists': True,
            }

    return _api_response(request, response_dict)

@view_config(route_name="api_user_suspend", renderer="jsonp")
def suspend_acct(request):
    """Reset a user account to enable them to change their password"""
    params = request.params
    user = request.user

    # we need to get the user from the email
    email = params.get('email', None)

    if email is None and hasattr(request, 'json_body'):
        # try the json body
        email = request.json_body.get('email', None)

    if user is None and email is None:
        request.response.status_int = 406
        return _api_response(request, {
            'error': "Please submit an email address",
        })

    if user is None and email is not None:
        user = UserMgr.get(email=email)

    if user is None:
        request.response.status_int = 404
        return _api_response(request, {
            'error': "Please submit a valid address",
            'email': email
        })

    # check if we've already gotten an activation for this user
    if user.activation is not None:
        request.response.status_int = 406
        return _api_response(request, {
            'error': """You've already marked your account for reactivation. Please check your email for the reactivation link. Make sure to check your spam folder.""",
            'username': user.username,
        })

    # mark them for reactivation
    user.reactivate("FORGOTTEN")

    # log it
    AuthLog.reactivate(user.username)

    # and then send an email notification
    # @todo the email side of things
    settings = request.registry.settings
    msg = ReactivateMsg(user.email,
                        "Activate your account",
                        settings)

    msg.send({
        'url': request.route_url(
            'reset',
            username=user.username,
            reset_key=user.activation.code),
        'username': user.username
    })

    return _api_response(request, {
        'message': """Your account has been marked for reactivation. Please check your email for instructions to reset your password.""",
    })


@view_config(route_name="api_user_suspend_remove", renderer="jsonp")
def account_activate(request):
    """Reset a user after being suspended

    :param username: required to know what user we're resetting
    :param activation: code needed to activate
    :param password: new password to use for the user

    """
    params = request.params

    username = params.get('username', None)
    activation = params.get('code', None)
    password = params.get('password', None)
    new_username = params.get('new_username', None)

    if username is None and activation is None and password is None:
        # then try to get the same fields out of a json body
        json_body = request.json_body
        username = json_body.get('username', None)
        activation = json_body.get('code', None)
        password = json_body.get('password', None)
        new_username = json_body.get('new_username', None)

    if not UserMgr.acceptable_password(password):
        request.response.status_int = 406
        return _api_response(request, {
            'error': "Come on, pick a real password please",
        })

    res = ActivationMgr.activate_user(username, activation, password)

    if res:
        # success so respond nicely
        AuthLog.reactivate(username, success=True, code=activation)

        # if there's a new username and it's not the same as our current
        # username, update it
        if new_username and new_username != username:
            try:
                user = UserMgr.get(username=username)
                user.username = new_username
            except IntegrityError, exc:
                request.response.status_int = 500
                return _api_response(request, {
                    'error': 'There was an issue setting your new username',
                    'exc': str(exc)
                })

        return _api_response(request, {
            'message': "Account activated, please log in.",
            'username': username,
        })
    else:
        AuthLog.reactivate(username, success=False, code=activation)
        request.response.status_int = 500
        return _api_response(request, {
            'error': "There was an issue attempting to activate this account.",
        })


@view_config(route_name="api_user_invite", renderer="jsonp")
@api_auth('api_key', UserMgr.get)
def invite_user(request):
    """Invite a new user into the system.

    :param username: user that is requested we invite someone
    :param email: email address of the new user

    """
    params = request.params

    email = params.get('email', None)
    user = request.user

    if not email:
        # try to get it from the json body
        email = request.json_body.get('email', None)

    if not email:
        # if still no email, I give up!
        request.response.status_int = 406
        return _api_response(request, {
            'username': user.username,
            'error': "Please submit an email address"
        })

    # first see if the user is already in the system
    exists = UserMgr.get(email=email)
    if exists:
        request.response.status_int = 406
        return _api_response(request, {
            'username': exists.username,
            'error': "This user is already a user!"
        })

    new_user = user.invite(email)
    if new_user:
        LOG.error(new_user.username)
        # then this user is able to invite someone
        # log it
        AuthLog.reactivate(new_user.username)

        # and then send an email notification
        # @todo the email side of things
        settings = request.registry.settings
        msg = InvitationMsg(new_user.email,
                            "Enable your account",
                            settings)

        msg.send(
            request.route_url(
                'reset',
                username=new_user.username,
                reset_key=new_user.activation.code))
        return _api_response(request, {
            'message': 'You have invited: ' + new_user.email
        })
    else:
        # you have no invites
        request.response.status_int = 406
        return _api_response(request, {
            'username': user.username,
            'error': "You have no invites left at this time."
        })


# @view_config(route_name="api_admin_readable_todo", renderer="jsonp")
# @api_auth('api_key', UserMgr.get, admin_only=True)
# def to_readable(request):
#     """Get a list of urls, hash_ids we need to readable parse"""
#     url_list = Bmark.query.outerjoin(Readable, Readable.bid == Bmark.bid).\
#         join(Bmark.hashed).\
#         options(contains_eager(Bmark.hashed)).\
#         filter(Readable.imported == None).all()
#
#     def data(urls):
#         """Yield out the results with the url in the data streamed."""
#         for url in urls:
#             d = dict(url)
#             d['url'] = url.hashed.url
#             yield d
#
#     return _api_response(request, {
#         'urls': [u for u in data(url_list)]
#     })


# @view_config(route_name="api_admin_readable_reindex", renderer="jsonp")
# @api_auth('api_key', UserMgr.get, admin_only=True)
# def readable_reindex(request):
#     """Force the fulltext index to rebuild
#
#     This loops through ALL bookmarks and might take a while to complete.
#
#     """
#     tasks.reindex_fulltext_allbookmarks.delay()
#     return _api_response(request, {
#         'success': True
#     })


@view_config(route_name="api_admin_accounts_inactive", renderer="jsonp")
@api_auth('api_key', UserMgr.get, admin_only=True)
def accounts_inactive(request):
    """Return a list of the accounts that aren't activated."""
    user_list = UserMgr.get_list(active=False)
    ret = {
        'count': len(user_list),
        'users': [dict(h) for h in user_list],
    }
    return _api_response(request, ret)


@view_config(route_name="api_admin_accounts_invites", renderer="jsonp")
@api_auth('api_key', UserMgr.get, admin_only=True)
def accounts_invites(request):
    """Return a list of the accounts that aren't activated."""
    user_list = UserMgr.get_list()
    ret = {
        'users': [(u.username, u.invite_ct) for u in user_list],
    }
    return _api_response(request, ret)


@view_config(route_name="api_admin_accounts_invites_add", renderer="jsonp")
@api_auth('api_key', UserMgr.get, admin_only=True)
def accounts_invites_add(request):
    """Set the number of invites a user has available.

    :matchdict username: The user to give these invites to.
    :matchdict count: The number of invites to give them.
    """
    rdict = request.matchdict
    username = rdict.get('username', None)
    count = rdict.get('count', None)

    if username is not None and count is not None:
        user = UserMgr.get(username=username)

        if user:
            user.invite_ct = count
            return _api_response(request, dict(user))
        else:
            request.response.status_int = 404
            ret = {'error': "Invalid user account."}
            return _api_response(request, ret)
    else:
        request.response.status_int = 400
        ret = {'error': "Bad request, missing parameters"}
        return _api_response(request, ret)


# @view_config(route_name="api_admin_imports_list", renderer="jsonp")
# @api_auth('api_key', UserMgr.get, admin_only=True)
# def import_list(request):
#     """Provide some import related data."""
#     import_list = ImportQueueMgr.get_list()
#     ret = {
#         'count': len(import_list),
#         'imports': [dict(h) for h in import_list],
#     }
#     return _api_response(request, ret)


# @view_config(route_name="api_admin_imports_reset", renderer="jsonp")
# @api_auth('api_key', UserMgr.get, admin_only=True)
# def import_reset(request):
#     """Reset an import to try again"""
#     rdict = request.matchdict
#     import_id = rdict.get('id', None)
#
#     if not id:
#         request.response.status_int = 400
#         ret = {'error': "Bad request, missing parameters"}
#         return _api_response(request, ret)
#
#     imp = ImportQueueMgr.get(int(import_id))
#     imp.status = 0
#     tasks.importer_process.delay(imp.id)
#
#     ret = {
#         'import': dict(imp)
#     }
#     return _api_response(request, ret)


@view_config(route_name="api_admin_users_list", renderer="jsonp")
@api_auth('api_key', UserMgr.get, admin_only=True)
def user_list(request):
    """Provide list of users in the system.

    Supported Query params: order, limit
    """
    params = request.params
    order = params.get('order', None)
    limit = params.get('limit', None)
    user_list = UserMgr.get_list(order=order, limit=limit)
    ret = {
        'count': len(user_list),
        'users': [dict(h) for h in user_list],
    }
    return _api_response(request, ret)


@view_config(route_name="api_admin_new_user", renderer="jsonp")
@api_auth('api_key', UserMgr.get, admin_only=True)
def new_user(request):
    """Add a new user to the system manually."""
    rdict = request.params

    u = User()

    u.username = unicode(rdict.get('username'))
    u.email = unicode(rdict.get('email'))
    passwd = get_random_word(8)
    u.password = passwd
    u.activated = True
    u.is_admin = False
    u.api_key = User.gen_api_key()

    try:
        DBSession.add(u)
        DBSession.flush()
        # We need to return the password since the admin added the user
        # manually.  This is only time we should have/give the original
        # password.
        ret = dict(u)
        ret['random_pass'] = passwd
        return _api_response(request, ret)

    except IntegrityError, exc:
        # We might try to add a user that already exists.
        LOG.error(exc)
        request.response.status_int = 400
        return _api_response(request, {
            'error': 'Bad Request: User exists.',
        })


@view_config(route_name="api_admin_del_user", renderer="jsonp")
@api_auth('api_key', UserMgr.get, admin_only=True)
def del_user(request):
    """Remove a bad user from the system via the api.

    For admin use only.

    Removes all of a user's bookmarks before removing the user.

    """
    mdict = request.matchdict

    # Submit a username.
    del_username = mdict.get('username', None)

    if del_username is None:
        LOG.error('No username to remove.')
        request.response.status_int = 400
        return _api_response(request, {
            'error': 'Bad Request: No username to remove.',
        })

    u = UserMgr.get(username=del_username)

    if not u:
        LOG.error('Username not found.')
        request.response.status_int = 404
        return _api_response(request, {
            'error': 'User not found.',
        })

    # try:
    #     # Delete all of the bmarks for this year.
    #     Bmark.query.filter(Bmark.username == u.username).delete()
    #     DBSession.delete(u)
    #     return _api_response(request, {
    #         'success': True,
    #         'message': 'Removed user: ' + del_username
    #     })
    # except Exception, exc:
    #     # There might be cascade issues or something that causes us to fail in
    #     # removing.
    #     LOG.error(exc)
    #     request.response.status_int = 500
    #     return _api_response(request, {
    #         'error': 'Bad Request: ' + str(exc)
    #     })


# @view_config(route_name="api_admin_bmark_remove", renderer="jsonp")
# @api_auth('api_key', UserMgr.get, admin_only=True)
# def admin_bmark_remove(request):
#     """Remove this bookmark from the system"""
#     rdict = request.matchdict
#     username = rdict.get('username')
#     hash_id = rdict.get('hash_id')
#
#     try:
#         bmark = BmarkMgr.get_by_hash(hash_id,
#                                      username=username)
#         print bmark
#         if bmark:
#             DBSession.delete(bmark)
#             return _api_response(request, {
#                 'message': "done",
#             })
#         else:
#             return _api_response(request, {
#                 'error': 'Bookmark not found.',
#             })
#
#     except NoResultFound:
#         request.response.status_code = 404
#         return _api_response(request, {
#             'error': 'Bookmark with hash id {0} not found.'.format(
#                 rdict['hash_id'])
#         })


@view_config(route_name="api_admin_applog", renderer="jsonp")
@api_auth('api_key', UserMgr.get, admin_only=True)
def admin_applog(request):
    """Return applog data for admin use."""
    rdict = request.GET

    # Support optional filter parameters
    days = int(rdict.get('days', 1))
    status = rdict.get('status', None)
    message = rdict.get('message', None)

    log_list = AppLogMgr.find(
        days=days,
        message_filter=message,
        status=status,
    )

    ret = {
        'count': len(log_list),
        'logs': [dict(l) for l in log_list],
    }
    return _api_response(request, ret)
