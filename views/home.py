from ~~~PROJNAME~~~.queue import tasks
from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

@view_config(route_name='home', renderer='~~~PROJNAME~~~:templates/auth/signup.mako')
def my_view(request):
#    tasks.add.delay(5,5)
    return {'project': '~~~PROJNAME~~~'}
