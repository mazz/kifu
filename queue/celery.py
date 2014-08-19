
from __future__ import absolute_import
from celery import Celery
from datetime import timedelta
from os import path

from celery.signals import worker_init

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Query

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

Base.query = DBSession.query_property(Query)

import logging
LOG = logging.getLogger(__name__)

#~~~~~~~~~~ GLOBAL CELERY ~~~~~~~~~~#
celery = None

def load_ini():
    global celery

    celery = Celery(
        "~~~PROJNAME~~~.queue",
        broker="amqp://",
        include=["~~~PROJNAME~~~.queue.tasks"]
    )

    celery.conf.update(
        CELERY_RESULT_BACKEND = "redis://",
        CELERY_TASK_SERIALIZER = 'json',
        CELERY_RESULT_SERIALIZER = 'json',
        CELERY_TIMEZONE = 'Canada/Eastern',
        CELERY_ENABLE_UTC = True,
        CELERY_TASK_RESULT_EXPIRES=3600,
        CELERY_ACCEPT_CONTENT = ['pickle', 'json', 'msgpack', 'yaml'],
        CELERYBEAT_SCHEDULE = {
        }
    )

@worker_init.connect
def bootstrap_pyramid(signal, sender):

    from pyramid.paster import bootstrap
    sender.app.settings = bootstrap(path.join(path.dirname(path.dirname(path.dirname(__file__))), "development.ini"))['registry'].settings
    print "sender.app.settings: " + str(sender.app.settings)

    #customize_settings(sender.app.settings)

    engine = sqlalchemy.create_engine(sender.app.settings['sqlalchemy.url'])
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

load_ini()

if __name__ == '__main__':
    celery.start()

