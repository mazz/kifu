import logging

from ~~~PROJNAME~~~.queue import tasks

from datetime import datetime
from pyramid.httpexceptions import HTTPFound
from pyramid.httpexceptions import HTTPNotFound
from pyramid.renderers import render_to_response
from pyramid.security import remember
from pyramid.security import forget
from pyramid.url import route_url
from pyramid.response import Response

from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError
from ~~~PROJNAME~~~.models import Base
from ~~~PROJNAME~~~.models import DBSession

from ~~~PROJNAME~~~.lib.applog import AuthLog
from ~~~PROJNAME~~~.models.auth import User
from ~~~PROJNAME~~~.models.auth import UserMgr

from ~~~PROJNAME~~~.models.auth import Activation
from ~~~PROJNAME~~~.models.auth import ActivationMgr

LOG = logging.getLogger(__name__)
max_cookie_age = (60 * 60 * 24 * 30)

@view_config(route_name="login", renderer="~~~PROJNAME~~~:templates/auth/login.mako")
def login(request):
    """Login the user to the system

    If not POSTed then show the form
    If error, display the form with the error message
    If successful, forward the user to their /recent

    Note: the came_from stuff we're not using atm. We'll clean out if we keep
    things this way

    """

    # in case they're already logged-in just send them to their profile page for now
    if request.user:
        headers = remember(request, request.user.id, max_age=max_cookie_age)
        return HTTPFound(location=request.route_url('user_account', username=request.user.username),headers=headers)

    login_url = route_url('login', request)
    referrer = request.url
    if referrer == login_url:
        referrer = '/'  # never use the login form itself as came_from

    came_from = request.params.get('came_from', referrer)

    message = ''
    email = ''
    password = ''
    headers = None
    max_cookie_age = (60 * 60 * 24 * 30)

    # import pdb; pdb.set_trace()

    if 'form.submitted' in request.params:
        email = request.params['email']
        password = request.params['password']

        LOG.debug(email)
        auth = UserMgr.get(email=email)
        LOG.debug(auth)
        LOG.debug(UserMgr.get_list())

        if auth and auth.validate_password(password) and auth.activated:
            # We use the Primary Key as our identifier once someone has
            # authenticated rather than the username.  You can change what is
            # returned as the userid by altering what is passed to remember.
            headers = remember(request, auth.id, max_age=max_cookie_age)
            auth.last_login = datetime.utcnow()

            # log the successful login
            AuthLog.login(auth.username, True)

            # we're always going to return a user to their own /recent after a
            # login
#             return HTTPFound(
#                 location=request.route_url(
#                     'user_bmark_recent',
#                     username=auth.username),
#                 headers=headers)

            return HTTPFound(
                location=request.route_url(
                    'user_account',
                    username=auth.username),
                headers=headers)

        # log the right level of problem
        if auth and not auth.validate_password(password):
            message = "Your login attempt has failed."
            AuthLog.login(email, False, password=password)

        elif auth and not auth.activated:
            message = "User account deactivated. Please check your email."
            AuthLog.login(email, False, password=password)
            AuthLog.disabled(email)

        elif auth is None:
            message = "Failed login"
            AuthLog.login(email, False, password=password)

    # in case they're already logged-in just send them to their profile page for now
    if request.user:
        headers = remember(request, request.user.id, max_age=max_cookie_age)
        return HTTPFound(
            location=request.route_url(
                'user_account',
                username=request.user.username),
            headers=headers)

    return {
        'message': message,
        'came_from': came_from,
        'email': email,
        'password': password,
    }

@view_config(route_name="logout", renderer="~~~PROJNAME~~~:templates/auth/login.mako")
def logout(request):
    headers = forget(request)
    return HTTPFound(location=route_url('login', request),
                     headers=headers)

@view_config(route_name='list_users', renderer='~~~PROJNAME~~~:templates/list_users.mako')
def list_users(request):
    try:
        users = DBSession.query(User)
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {'users': users}

@view_config(route_name="signup", renderer="~~~PROJNAME~~~:templates/auth/signup.mako")
def signup(request):
    """Process the signup request

    If there are any errors drop to the same template with the error
    information.

    """

    message = ''

    # import pdb; pdb.set_trace()
    if request.user and request.user.username:
        print("user logged in")
        return HTTPFound(location=request.route_url('user_account', username=request.user.username))
    else:
        if request.method == 'POST':
            email = request.params['email']
            # password = request.params['password']

            LOG.debug(email)
            auth = UserMgr.get(email=email)

            if auth:
                return {
                    'email': '',
                    'message': 'A user with this email already exists.',
                }

            message = 'Thank you for signing up from: ' + str(email) + '\nPlease check your email.'
            request.session.flash(message)

            #return HTTPFound(location=request.route_url('signup_process2'))
            new_user = UserMgr.signup_user(email, 'signup')
            print "new_user: " + str(new_user)
            if new_user:
                AuthLog.reactivate(new_user.username)
                # @todo the email side of things
                settings = request.registry.settings

                # Add a queue job to send the user a notification email.
                tasks.email_signup_user.delay(
                   new_user.email,
                   "Enable your account",
                   settings,
                   request.route_url(
                       'reset',
                       username=new_user.username,
                       reset_key=new_user.activation.code
                   )
                )

                # And let the user know they're signed up.
                return {'message': message,
                        'email':email,
                }

        return {'email': '',
                'message': message,
                }

@view_config(route_name="forgot_password", renderer="~~~PROJNAME~~~:templates/auth/forgot.mako")
def forgot_password(request):
    """Login the user to the system

    If not POSTed then show the form
    If error, display the form with the error message
    If successful, forward the user to their /recent

    Note: the came_from stuff we're not using atm. We'll clean out if we keep
    things this way

    """
    # in case they're already logged-in just send them to their profile page for now
    if request.user:
        headers = remember(request, request.user.id, max_age=max_cookie_age)
        return HTTPFound(location=request.route_url('user_account', username=request.user.username),headers=headers)

    fp_url = route_url('forgot_password', request)
    referrer = request.url
    if referrer == fp_url:
        referrer = '/'  # never use the login form itself as came_from
    came_from = request.params.get('came_from', referrer)
    #
    message = ''
    # login = ''
    # password = ''

    # import pdb; pdb.set_trace()

    if 'form.submitted' in request.params:
        email = request.params['email']
        # password = request.params['password']

        LOG.debug(email)
        user = UserMgr.get(email=email)
        LOG.debug(user)
        # LOG.debug(UserMgr.get_list())

        settings = request.registry.settings

        if user:
            # Add a queue job to send the user a notification email.
            user.reactivate('forgot_password')
            tasks.email_forgot_password_user.delay(
                user.email,
                "Reset Your Password",
                settings,
                request.route_url(
                'reset',
                username=user.username,
                reset_key=user.activation.code)
            )

            message = 'An email has been sent with instructions for resetting your password. If you do not receive it within an hour or two, check your spam folder.'
            # # We use the Primary Key as our identifier once someone has
            # # authenticated rather than the username.  You can change what is
            # # returned as the userid by altering what is passed to remember.
            # headers = remember(request, auth.id, max_age=60 * 60 * 24 * 30)
            # auth.last_login = datetime.utcnow()
            #
            # # log the successful login
            # AuthLog.login(login, True)

            # we're always going to return a user to their own /recent after a
            # login
#             return HTTPFound(
#                 location=request.route_url(
#                     'user_bmark_recent',
#                     username=auth.username),
#                 headers=headers)

            # return HTTPFound(
            #     location=request.route_url(
            #         'forgot_password_email_confirmed'),
            #     headers=headers)

        if not user:
            message = 'There was an error attempting to find that email.'
        # log the right level of problem
        # if auth and not auth.validate_password(password):
        #     message = "Your login attempt has failed."
        #     AuthLog.login(login, False, password=password)
        #
        # elif auth and not auth.activated:
        #     message = "User account deactivated. Please check your email."
        #     AuthLog.login(login, False, password=password)
        #     AuthLog.disabled(login)
        #
        # elif auth is None:
        #     message = "Failed login"
        #     AuthLog.login(login, False, password=password)
    return {
        'message': message,
        'came_from': came_from,
    }


@view_config(route_name="reset", renderer="~~~PROJNAME~~~:templates/auth/reset.mako")
def reset(request):
    """Once deactivated, allow for changing the password via activation key"""
    rdict = request.matchdict
    params = request.params

    message = ''

    # This is an initial request to show the activation form.
    username = rdict.get('username', None)
    activation_key = rdict.get('reset_key', None)
    user = ActivationMgr.get_user(username, activation_key)

    if user is None:
        # just 404 if we don't have an activation code for this user
        raise HTTPNotFound()

    if 'code' in params:
        # This is a posted form with the activation, attempt to unlock the
        # user's account.
        username = params.get('username', None)
        activation = params.get('code', None)
        password1 = params.get('password1', None)
        password2 = params.get('password2', None)
        new_username = params.get('new_username', None)

        res = ActivationMgr.activate_user(username, activation, password1)
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
                    message = 'There was an issue setting your new username. Please try again.'
        else:
            AuthLog.reactivate(username, success=False, code=activation)
            message = 'There was an issue attempting to activate this account.'

        if message is not '':
            return {
                'message': message,
                'user': user
            }
        else:
            # log the user out to have them re-login with the new password
            headers = forget(request)
            return HTTPFound(location=route_url('login', request),
                             headers=headers)

            # headers = remember(request, user.id, max_age=60 * 60 * 24 * 30)
            # user.last_login = datetime.utcnow()
            #
            # # log the successful login
            # AuthLog.login(user.username, True)
            #
            # # we're always going to return a user to their own /recent after a
            # # login
            # return HTTPFound(
            #     location=request.route_url(
            #         'user_account',
            #         username=user.username),
            #     headers=headers)

    else:
        LOG.error("CHECKING")
        LOG.error(username)

        if user is None:
            # just 404 if we don't have an activation code for this user
            raise HTTPNotFound()

        LOG.error(user.username)
        LOG.error(user.email)
        return {
            'message': message,
            'user': user,
        }

conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_~~~PROJNAME~~~_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
