from datetime import datetime
from datetime import timedelta

from sqlalchemy import engine_from_config
from sqlalchemy import event
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import Unicode
from sqlalchemy import UnicodeText
from sqlalchemy import ForeignKey
from sqlalchemy import Table
from sqlalchemy import select
from urlparse import urlparse

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import aliased
from sqlalchemy.orm import contains_eager
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import relation
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Query
from sqlalchemy.orm.exc import NoResultFound

from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy.sql import func
from sqlalchemy.sql import and_

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

from .applog import AppLog
from .auth import User, Activation

def initialize_sql(settings):
    """Called by the app on startup to setup bindings to the DB"""
    engine = engine_from_config(settings, 'sqlalchemy.')

    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

#    import bookie.models.fulltext as ft
#    ft.set_index(settings.get('fulltext.engine'),
#                 settings.get('fulltext.index'))

    # setup the User relation, we've got import race conditions, ugh
#    from bookie.models.auth import User
#    if not hasattr(Bmark, 'user'):
#        Bmark.user = relation(User,
#                              backref="bmark")

def todict(self):
    """Method to turn an SA instance into a dict so we can output to json"""

    def convert_datetime(value):
        """We need to treat datetime's special to get them to json"""
        if value:
            return value.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return ""

    for col in self.__table__.columns:
        if isinstance(col.type, DateTime):
            value = convert_datetime(getattr(self, col.name))
        else:
            value = getattr(self, col.name)

        yield(col.name, value)


def iterfunc(self):
    """Returns an iterable that supports .next()
        so we can do dict(sa_instance)

    """
    return self.__todict__()


def fromdict(self, values):
    """Merge in items in the values dict into our object

       if it's one of our columns

    """
    for col in self.__table__.columns:
        if col.name in values:
            setattr(self, col.name, values[col.name])

Base.query = DBSession.query_property(Query)
Base.__todict__ = todict
Base.__iter__ = iterfunc
Base.fromdict = fromdict
