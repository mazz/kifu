
from __future__ import absolute_import

from &&PROJNAME&&.queue.celery import celery
#from celery import Celery

from .celery import load_ini
INI = load_ini()

@celery.task
def add(x, y):
    return x + y
