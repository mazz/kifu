from __future__ import absolute_import
from celery import Celery
from celery.signals import worker_init


@worker_init.connect
def bootstrap_pyramid(signal, sender):
    import os
    from pyramid.paster import bootstrap
    #sender.app.settings = bootstrap(os.environ['development.ini'])['registry'].settings
    print "os.environ: " + str(os.environ)
    #print "sender.app.settings: " + sender.app.settings

celery = Celery()
#celery.config_from_object('celeryconfig')

celery.conf.update(
    BROKER_URL = 'amqp://',
    CELERY_RESULT_BACKEND = "redis://",
    CELERY_TASK_SERIALIZER = "json",
    CELERY_RESULT_SERIALIZER = "json",
    CELERY_TIMEZONE = "Canada/Eastern",
    CELERY_ENABLE_UTC = True,
    CELERY_TASK_RESULT_EXPIRES=3600
)

if __name__ == '__main__':
    celery.start()

#celery = Celery()
#celery.config_from_object('default.queue.celeryconfig')

