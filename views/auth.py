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

from ~~~PROJNAME~~~.models.auth import User
from ~~~PROJNAME~~~.models.auth import UserMgr

from ~~~PROJNAME~~~.models.auth import Activation
from ~~~PROJNAME~~~.models.auth import ActivationMgr

LOG = logging.getLogger(__name__)

@view_config(route_name='list_users', renderer='~~~PROJNAME~~~:templates/list_users.mako')
def my_view(request):
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
    params = request.params
    email = params.get('email', None)

    if not email:
        # if still no email, I give up!
        return {
            'errors': {
                'email': 'Please supply an email address to sign up.'
            }
        }

    # first see if the user is already in the system
    exists = UserMgr.get(email=email)
    if exists:
        return {
            'errors': {
                'email': 'The user has already signed up.'
            }
        }

    new_user = UserMgr.signup_user(email, 'signup')
    print "new_user: " + str(new_user)
    if new_user:
        # then this user is able to invite someone
        # log it
#        AuthLog.reactivate(new_user.username)

        # and then send an email notification
        # @todo the email side of things
        settings = request.registry.settings

        # Add a queue job to send the user a notification email.
#        tasks.email_signup_user.delay(
#            new_user.email,
#            "Enable your Bookie account",
#            settings,
#            request.route_url(
#                'reset',
#                username=new_user.username,
#                reset_key=new_user.activation.code
#            )
#        )

        # And let the user know they're signed up.
        return {
            'message': 'Thank you for signing up from: ' + new_user.email
        }
    else:
        return {
            'errors': {
                'email': 'There was an unknown error signing up.'
            }
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
                #AuthLog.reactivate(username, success=True, code=activation)

                # if there's a new username and it's not the same as our current
                # username, update it
                if new_username and new_username != username:
                    try:
                        user = UserMgr.get(username=username)
                        user.username = new_username
                    except IntegrityError, exc:
                        error = 'There was an issue setting your new username'
            else:
                #AuthLog.reactivate(username, success=False, code=activation)
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
            #AuthLog.login(user.username, True)

            # we're always going to return a user to their own /recent after a
            # login
            return HTTPFound(
                location=request.route_url(
                    'list_users',
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
