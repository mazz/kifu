from __future__ import absolute_import

from ~~~PROJNAME~~~.queue.celery import celery
import transaction

#from celery import Celery

# from .celery import load_ini
# INI = load_ini()

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
    from ~~~PROJNAME~~~.lib.message import InvitationMsg
    msg = InvitationMsg(email, msg, settings)
    status = msg.send(message_data)
    if status == 4:
#        from bookie.lib.applog import SignupLog
        trans = transaction.begin()
        LOG.info('Could not send smtp email to signup: ' + email)
        trans.commit()

