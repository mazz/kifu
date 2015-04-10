from __future__ import absolute_import

from ~~~PROJNAME~~~.queue.celery import celery
import transaction
import os
from os import path
from ConfigParser import ConfigParser
import json
import requests
from ~~~PROJNAME~~~.models.auth import UserMgr

import logging
LOG = logging.getLogger(__name__)

@celery.task
def add(x, y):
    return x + y

@celery.task(ignore_result=True)
def email_signup_user(email, msg, settings, message_data):
    """Do the real import work

    :param iid: import id we need to pull and work on

    """

    from ~~~PROJNAME~~~.lib.msg import SignupMsg
    msg = SignupMsg(email, msg, settings)
    status = msg.send(message_data)
    LOG.info('email sending status: ' + repr(status))

    if status == 4:
        from foo.lib.applog import SignupLog
        trans = transaction.begin()
        LOG.info('Could not send smtp email to signup: ' + email)
        trans.commit()

@celery.task(ignore_result=True)
def email_forgot_password_user(email, msg, settings, message_data):
    """Do the real import work

    :param iid: import id we need to pull and work on

    """
    from ~~~PROJNAME~~~.lib.msg import ResetMsg
    msg = ResetMsg(email, msg, settings)
    status = msg.send(message_data)
    if status == 4:
        from lrd.lib.applog import SignupLog
        trans = transaction.begin()
        LOG.info('Could not send smtp email to signup: ' + email)
        trans.commit()

    # if email is not None:
    #     server_dict = _server_and_port()
    #     endpoint = 'http://' + server_dict['host'] + ':' + str(server_dict['port']) + '/api/v1/suspend'
    #     headers = {'content-type': 'application/json'}
    #
    #     print('endpoint: ' + repr(endpoint))
    #     payload = {'email': email}
    #     print('payload: ' + repr(payload))
    #     post_response = requests.post(endpoint, data=json.dumps(payload), headers=headers)
    #
    # else:
    #     LOG.error('email is None')
    #
    # message = post_response.json().get('message', None)
    # error = post_response.json().get('error', None)
    #
    # print('post_response message: ' + repr(message))
    # print('post_response error: ' + repr(error))
    #
    # ret = {}
    # if message is not None:
    #     ret['message'] = message
    # else:
    #     ret['message'] = error
    #
    # return ret
@celery.task(ignore_result=False)
def username_exists(username):
    user = UserMgr.get(username=username)

    response_dict = {}
    if user is None:
        response_dict['exists'] = False
    else:
        response_dict['exists'] = True
    return response_dict


@celery.task(ignore_result=True)
def test_post():
    endpoint = 'http://posttestserver.com/post.php'
    headers = {'content-type': 'application/json'}

    payload = {'dir': 'maz'}
    response = requests.post(endpoint, data=json.dumps(payload), headers=headers)
    print('response: ' + str(response))

def _server_and_port():
    pyramid_env = os.environ.get('PYRAMID_ENV', 'development')

    if pyramid_env == 'production':
        ini_path = path.join(path.dirname(path.dirname(path.dirname(__file__))), "production.ini")
    else:
        ini_path = path.join(path.dirname(path.dirname(path.dirname(__file__))), "development.ini")

    cfg = ConfigParser()
    cfg.readfp(open(ini_path))
    # Hold onto the ini config.

    server_dict = dict(cfg.items('server:main', raw=True))
    return server_dict
