import contextlib

from pyramid.paster import get_appsettings
from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker, scoped_session


def get_session(scoped=False):
    settings = get_appsettings('development.ini')
    engine = engine_from_config(settings, 'sqlalchemy.')
    Session = scoped_session(
        sessionmaker(
            bind=engine,
            expire_on_commit=False,  # god damn DetachedInstanceError
        )
    )
    if scoped:
        Session = scoped_session(Session)
    return Session()


@contextlib.contextmanager
def session_context():
    session = None
    try:
        session = get_session(scoped=True)
        yield session
        session.commit()
    except:
        if session is not None:
            session.rollback()
        raise
