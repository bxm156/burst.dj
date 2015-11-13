import contextlib

import transaction
from pyramid.paster import get_appsettings
from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker, scoped_session
from zope.sqlalchemy import ZopeTransactionExtension


def get_session():
    settings = get_appsettings('development.ini')
    engine = engine_from_config(settings, 'sqlalchemy.')
    Session = scoped_session(sessionmaker(bind=engine, extension=ZopeTransactionExtension()))
    return Session()

@contextlib.contextmanager
def session_context():
    try:
        session = get_session()
        transaction.begin()
        yield session
        transaction.commit()
    except:
        transaction.abort()
