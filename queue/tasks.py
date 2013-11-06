import celery
from celery import Celery

@celery.task
def add(x, y):
    return x + y
