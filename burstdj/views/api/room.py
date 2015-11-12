from collections import defaultdict

from pyramid.exceptions import Forbidden
from pyramid.security import authenticated_userid, effective_principals
from pyramid.view import view_config

from cornice import Service



room_activity = Service(name='room_activity', path='/room/{room_id}/activity')

_USERS = defaultdict(dict)


@room_activity.get()
def get_room_activity(request):
    """Return what's going on in this room.  This includes current track
    (most important) and the room's users.
    """
    room_id = request.matchdict['room_id']

    # TODO: fetch current track for room

    # TODO: fetch users in room

    return dict(
        room_id=room_id,
        current_track=None,
        users=[],
    )
