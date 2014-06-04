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

from ~~~PROJNAME~~~.forms.signupform import SignupForm

LOG = logging.getLogger(__name__)

@view_config(route_name="login", renderer="~~~PROJNAME~~~:templates/auth/login.mako")
def login(request):
    """Login the user to the system

    If not POSTed then show the form
    If error, display the form with the error message
    If successful, forward the user to their /recent

    Note: the came_from stuff we're not using atm. We'll clean out if we keep
    things this way

    """
    login_url = route_url('login', request)
    referrer = request.url
    if referrer == login_url:
        referrer = '/'  # never use the login form itself as came_from

    came_from = request.params.get('came_from', referrer)

    message = ''
    login = ''
    password = ''

    if 'form.submitted' in request.params:
        login = request.params['login']
        password = request.params['password']

        LOG.debug(login)
        auth = UserMgr.get(username=login)
        LOG.debug(auth)
        LOG.debug(UserMgr.get_list())

        if auth and auth.validate_password(password) and auth.activated:
            # We use the Primary Key as our identifier once someone has
            # authenticated rather than the username.  You can change what is
            # returned as the userid by altering what is passed to remember.
            headers = remember(request, auth.id, max_age=60 * 60 * 24 * 30)
            auth.last_login = datetime.utcnow()

            # log the successful login
            AuthLog.login(login, True)

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
            AuthLog.login(login, False, password=password)

        elif auth and not auth.activated:
            message = "User account deactivated. Please check your email."
            AuthLog.login(login, False, password=password)
            AuthLog.disabled(login)

        elif auth is None:
            message = "Failed login"
            AuthLog.login(login, False, password=password)

    return {
        'message': message,
        'came_from': came_from,
        'login': login,
        'password': password,
    }


@view_config(route_name="logout", renderer="~~~PROJNAME~~~:templates/auth/login.mako")
def logout(request):
    headers = forget(request)
    return HTTPFound(location=route_url('signup_process', request),
                     headers=headers)

@view_config(route_name='list_users', renderer='~~~PROJNAME~~~:templates/list_users.mako')
def list_users(request):
    try:
        users = DBSession.query(User)
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {'users': users}

@view_config(route_name="signup_process", renderer="~~~PROJNAME~~~:templates/auth/signup.mako")
def signup_process(request):
    """Process the signup request

    If there are any errors drop to the same template with the error
    information.

    """
    if request.user and request.user.username:
        print("user logged in")
        return HTTPFound(location=request.route_url('user_account', username=request.user.username))
    else:
        signupForm = SignupForm(request.POST)

        if request.method == 'POST' and signupForm.validate():
            message = 'Thank you for signing up from: ' + str(signupForm.email.data) + '\nPlease check your email.'
            request.session.flash(message)

            #return HTTPFound(location=request.route_url('signup_process2'))
            new_user = UserMgr.signup_user(signupForm.email.data, 'signup')
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
                return {'signup_success_message': message,
                        'form':signupForm,
                }

        return {'form':signupForm,
                'action':request.matchdict.get('action'),
                }

@view_config(route_name="reset", renderer="~~~PROJNAME~~~:templates/auth/reset.mako")
def reset(request):
    """Once deactivated, allow for changing the password via activation key"""
    rdict = request.matchdict
    params = request.params

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
        password = params.get('new_password', None)
        new_username = params.get('new_username', None)
        error = None

        if not UserMgr.acceptable_password(password):
            # Set an error message to the template.
            error = "Come on, pick a real password please."
        else:
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
                        error = 'There was an issue setting your new username'
            else:
                AuthLog.reactivate(username, success=False, code=activation)
                error = 'There was an issue attempting to activate this account.'

        if error:
            return {
                'message': error,
                'user': user
            }
        else:
            # Log the user in and move along.
            headers = remember(request, user.id, max_age=60 * 60 * 24 * 30)
            user.last_login = datetime.utcnow()

            # log the successful login
            AuthLog.login(user.username, True)

            # we're always going to return a user to their own /recent after a
            # login
            return HTTPFound(
                location=request.route_url(
                    'user_account',
                    username=user.username),
                headers=headers)

    else:
        LOG.error("CHECKING")
        LOG.error(username)

        if user is None:
            # just 404 if we don't have an activation code for this user
            raise HTTPNotFound()

        LOG.error(user.username)
        LOG.error(user.email)
        return {
            'user': user,
        }

conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_foo_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
