from collections import defaultdict
from cornice import Service

from burstdj.logic import security

rooms = Service(
    name='rooms',
    path='/api/room',
    permission='authenticated',
)

room = Service(
    name='room',
    path='/api/room/{room_id}',
    permission='authenticated',
)

room_join = Service(
    name='room',
    path='/api/room/{room_id}/join',
    permission='authenticated',
)

room_activity = Service(
    name='room_activity',
    path='/api/room/{room_id}/activity',
    permission='authenticated',
)

_USERS = defaultdict(dict)


@rooms.post()
def post_room(request):
    user_id = security.current_user_id(request)
    pass

@rooms.get()
def list_rooms(request):
    pass

@room_join.post()
def join_room(request):
    pass

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
