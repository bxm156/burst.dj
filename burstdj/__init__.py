from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from burstdj.logic import security
from burstdj.models import (
    DBSession,
    Base,
)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(
        settings=settings,
        root_factory='burstdj.logic.security.RootFactory',
    )
    config.include('pyramid_chameleon')
    config.include('cornice')

    # Security policies
    authn_policy = AuthTktAuthenticationPolicy(
        settings['authentication.secret'],
        callback=security.groupfinder,
        hashalg='sha512'
    )
    authz_policy = ACLAuthorizationPolicy()
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)

    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('login', '/login')
    config.add_route('find_room', '/find_room')
    config.add_route('room', '/room')
    config.add_route('logout', '/logout')
    config.add_route('whoami', '/whoami')

    config.scan()
    return config.make_wsgi_app()
