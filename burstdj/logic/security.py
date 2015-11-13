from pyramid.security import Allow, Authenticated
from pyramid.security import Everyone


"""username to password"""
USERS = {
    'jcontemp': '',
    'bmarty': '',
    'ptiet': '',
    'markon': '',
    'rroeder': '',
}

"""username to list of groups"""
GROUPS = {
    'jcontemp': [
        'group:admin'
    ],
}


def is_request_authenticated(request):
    return bool(request.authenticated_userid)

def groupfinder(userid, request):
    """This is where we'd verify the user exists.  return None if not."""
    if userid in USERS:
        return GROUPS.get(userid, [])


class RootFactory(object):
    """match groups to permissions"""
    __acl__ = [
        (Allow, Everyone, 'view'),
        (Allow, Authenticated, 'authenticated'),
        (Allow, 'group:admin', 'admin'),
    ]
    def __init__(self, request):
        pass
