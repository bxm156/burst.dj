from cornice import Service
from burstdj.core.error import HTTPBadRequest, HTTPConflict

from burstdj.logic import security
from burstdj.logic import room as room_logic
from burstdj.logic.room import RoomAlreadyExists

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
    name='room_join',
    path='/api/room/{room_id}/join',
    permission='authenticated',
)

queue_join = Service(
    name='room_queue_join',
    path='/api/room/{room_id}/queue/join',
    permission='authenticated',
)

room_activity = Service(
    name='room_activity',
    path='/api/room/{room_id}/activity',
    permission='authenticated',
)


@rooms.post()
def post_room(request):
    name = request.json_body.get('name', None)
    if name is None:
        raise HTTPBadRequest()
    user_id = security.current_user_id(request)
    try:
        room = room_logic.create_room(name, user_id)
    except RoomAlreadyExists:
        raise HTTPConflict()
    return dict(
        id=room.id,
        name=room.name,
        time_created=room.time_created.isoformat(),
    )

@rooms.get()
def list_rooms(request):
    rooms = room_logic.list_rooms()
    return [
        dict(id=room.id, name=room.name, user_count=room.user_count) for room in rooms
    ]

@room_join.post()
def join_room(request):
    room_id = request.matchdict['room_id']
    try:
        room_id = int(room_id)
    except:
        raise HTTPBadRequest()
    user_id = security.current_user_id(request)
    room = room_logic.join_room(room_id, user_id)
    return dict(
        id=room.id,
        name=room.name,
        users=[
            dict(id=user.id, name=user.name, avatar=user.avatar_url)
            for user in room.users
        ]
    )


@queue_join.post()
def join_queue(request):
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
