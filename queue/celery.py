from __future__ import absolute_import
from celery import Celery
from ConfigParser import ConfigParser
from datetime import timedelta
from os import environ
from os import path

from celery.signals import worker_init

def load_ini():
    print "load_ini"
    cfg = ConfigParser()
    ini_path = path.join(path.dirname(path.dirname(path.dirname(__file__))), "development.ini")
    print "ini_path: " + ini_path

    cfg.readfp(open(ini_path))
    # Hold onto the ini config.
    return dict(cfg.items('app:main', raw=True))

#@worker_init.connect
#def bootstrap_pyramid(signal, sender):
#    import os
#    from pyramid.paster import bootstrap
#    #sender.app.settings = bootstrap(os.environ['development.ini'])['registry'].settings
#    print "signal: " + str(signal)
#    print "sender: " + str(sender)
#    print "os.environ: " + str(os.environ)
#    #print "sender.app.settings: " + sender.app.settings

INI = load_ini()

celery = Celery(
    "~~~PROJNAME~~~.queue",
    broker="amqp://",
    include=["~~~PROJNAME~~~.queue.tasks"])

celery.conf.update(
    CELERY_RESULT_BACKEND = "redis://",
    CELERY_TASK_SERIALIZER = 'json',
    CELERY_RESULT_SERIALIZER = 'json',
    CELERY_TIMEZONE = 'Canada/Eastern',
    CELERY_ENABLE_UTC = True,
    CELERY_TASK_RESULT_EXPIRES=3600,
    CELERY_ACCEPT_CONTENT = ['pickle', 'json', 'msgpack', 'yaml']
)

if __name__ == '__main__':
    celery.start()

