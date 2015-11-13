import contextlib

import transaction
from pyramid.paster import get_appsettings
from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker, scoped_session
from zope.sqlalchemy import ZopeTransactionExtension


def get_session(scoped=False):
    settings = get_appsettings('development.ini')
    engine = engine_from_config(settings, 'sqlalchemy.')
    Session = sessionmaker(bind=engine, extension=ZopeTransactionExtension())
    if scoped:
        Session = scoped_session(Session)

    return Session()

@contextlib.contextmanager
def session_context():
    try:
        session = get_session(scoped=True)
        transaction.begin()
        yield session
        transaction.commit()
    except:
        transaction.abort()
        raise
