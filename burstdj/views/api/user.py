from collections import defaultdict

from pyramid.exceptions import Forbidden
from pyramid.security import authenticated_userid, effective_principals
from pyramid.view import view_config

from cornice import Service

from burstdj.logic import security

current_user = Service(name='current_user', path='/api/current_user', permission='authenticated')


@current_user.get()
def get_current_user(request):
    user = security.get_current_user(request)
    return dict(
        id=user.id,
        name=user.name,
        avatar=user.avatar_url,
    )

@view_config(route_name="whoami", permission="authenticated", renderer="json")
def whoami(request):
    """View returning the authenticated user's credentials."""
    username = authenticated_userid(request)
    principals = effective_principals(request)
    return {"username": username, "principals": principals}