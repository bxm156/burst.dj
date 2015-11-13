from pyramid.security import Allow, Authenticated, remember
from pyramid.security import Everyone

from burstdj import db
from burstdj.models.user import User

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


def lookup_or_add_user(username):
    with db.session_context() as session:
        user = session.query(User).filter(User.name == username).first()
        if user is None:
            user = User(name=username)
            session.add(user)
            session.flush([user])
        session.expunge(user)
    return user


def lookup_user_by_id(user_id):
    session = db.get_session()
    return session.query(User).filter(User.id == user_id).first()

def list_users():
    session = db.get_session()
    return session.query(User).all()


def get_current_user(request):
    user_id = current_user_id(request)
    return lookup_user_by_id(user_id)


def authenticate_user(request, username):
    # lol YOLO
    user = lookup_or_add_user(username)
    headers = remember(request, user.id)
    return headers

def current_user_id(request):
    return request.authenticated_userid

def is_request_authenticated(request):
    return bool(request.authenticated_userid)

def groupfinder(userid, request):
    """This is where we'd return groups.  return None if user's invalid."""
    return []


class RootFactory(object):
    """match groups to permissions"""
    __acl__ = [
        (Allow, Everyone, 'view'),
        (Allow, Authenticated, 'authenticated'),
        (Allow, 'group:admin', 'admin'),
    ]
    def __init__(self, request):
        pass
