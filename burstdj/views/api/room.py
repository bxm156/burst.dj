from cornice import Service
from burstdj.core.error import HTTPBadRequest, HTTPConflict, HTTPNotFound, \
    HTTPForbidden

from burstdj.logic import security
from burstdj.logic import room as room_logic
from burstdj.logic.room import RoomAlreadyExists, UserNotInRoom, RoomNotFound

# POST: create a new room
# GET: list all rooms
rooms = Service(
    name='rooms',
    path='/api/room',
    permission='authenticated',
)

# join a room (observe)
room_join = Service(
    name='room_join',
    path='/api/room/{room_id}/join',
    permission='authenticated',
)

# join the queue in a room (actively DJ)
queue_join = Service(
    name='queue_join',
    path='/api/room/{room_id}/queue/join',
    permission='authenticated',
)

# join the queue in a room (no longer DJ)
queue_leave = Service(
    name='queue_leave',
    path='/api/room/{room_id}/queue/leave',
    permission='authenticated',
)

# fetch the current activity for a room (poll)
room_activity = Service(
    name='room_activity',
    path='/api/room/{room_id}/activity',
    permission='authenticated',
)

# # fetch the details for a room (this is redundant with activity)
# room = Service(
#     name='room',
#     path='/api/room/{room_id}',
#     permission='authenticated',
# )


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
    try:
        room = room_logic.join_room(room_id, user_id)
    except RoomNotFound:
        raise HTTPNotFound()
    return dict(
        id=room.id,
        name=room.name,
        users=serialize_users(room.users)
    )


@queue_join.post()
def join_queue(request):
    room_id = request.matchdict['room_id']
    try:
        room_id = int(room_id)
    except:
        raise HTTPBadRequest()
    user_id = security.current_user_id(request)
    try:
        newly_joined = room_logic.join_queue(room_id, user_id)
    except UserNotInRoom:
        raise HTTPForbidden()
    except RoomNotFound:
        raise HTTPNotFound()
    return dict(
        success=True,
        newly_joined=newly_joined,
    )


@queue_leave.post()
def leave_queue(request):
    room_id = request.matchdict['room_id']
    try:
        room_id = int(room_id)
    except:
        raise HTTPBadRequest()
    user_id = security.current_user_id(request)
    try:
        newly_bounced = room_logic.leave_queue(room_id, user_id)
    except UserNotInRoom:
        raise HTTPForbidden()
    except RoomNotFound:
        raise HTTPNotFound()
    return dict(
        success=True,
        newly_bounced=newly_bounced,
    )


@room_activity.get()
def get_room_activity(request):
    """Return what's going on in this room.  This includes current track
    (most important) and the room's users.
    """
    room_id = request.matchdict['room_id']

    # TODO: fetch current track for room.  this needs to be fleshed out
    room = room_logic.get_current_room_track(room_id)
    track = room.track

    # fetch users in room, in order of joining
    users = room_logic.list_room_users(room_id)

    # fetch DJs in room, in order of who will play next
    djs = room_logic.list_room_djs(room_id)

    return dict(
        room=dict(
            id=room_id,
            name=room.name,
        ),
        track=serialize_track(track, time_started=room.time_track_started),
        users=serialize_users(users),
        djs=serialize_users(djs),
        current_dj_id=room.current_user_id,
    )


def serialize_track(track, time_started=None):
    if track is None:
        return None
    time_started = None if time_started is None else time_started.isoformat()
    return dict(
        id=track.id,
        name=track.name,
        provider_track_id=track.provider_track_id,
        provider=track.provider,
        time_started=time_started,
        length=track.length,
    )

def serialize_users(users):
    return [serialize_user(user) for user in users]

def serialize_user(user):
    return dict(id=user.id, name=user.name, avatar=user.avatar_url)