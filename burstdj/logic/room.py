from sqlalchemy import desc
from sqlalchemy.sql.functions import count

from burstdj import db
from burstdj.models.room import Room
from burstdj.models.room_queue import RoomQueue
from burstdj.models.room_user import RoomUser
from burstdj.models.user import User


class RoomAlreadyExists(Exception):
    pass

class RoomNotFound(Exception):
    pass

class UserNotInRoom(Exception):
    pass


def create_room(name, user_id):
    with db.session_context() as session:
        room = session.query(Room).filter(Room.name == name).first()
        if room is not None:
            raise RoomAlreadyExists(room)
        room = Room(
            name=name,
            admin_user_id=user_id,
        )
        session.add(room)
        session.flush([room])
    return room


def list_rooms(limit=20, offset=0):
    """List the most popular rooms."""
    with db.session_context() as session:
        results = session.query(
            Room,
            (count(RoomUser.id)),
        ).outerjoin(
            RoomUser
        ).group_by(
            Room
        ).order_by(
            desc(count(RoomUser.id)),
            Room.name,
        ).limit(
            limit
        ).offset(
            offset
        ).all()
    rooms = []
    for result in results:
        room = result[0]
        room.user_count = result[1]
        rooms.append(room)
    return rooms


def _leave_rooms(session, user_id):
    session.query(
        RoomUser,
    ).filter(
        RoomUser.user_id == user_id
    ).delete()

    session.query(
        RoomQueue,
    ).filter(
        RoomQueue.user_id == user_id
    ).delete()


def join_room(room_id, user_id):
    with db.session_context() as session:
        if not _does_room_exist(session, room_id):
            raise RoomNotFound()

        _leave_rooms(session, user_id)

        # join room
        room_user = RoomUser(
            room_id=room_id,
            user_id=user_id,
        )
        session.add(room_user)
        session.flush()

        room = session.query(Room).filter(Room.id == room_id).first()
        users = session.query(
            User
        ).join(
            RoomUser
        ).filter(
            RoomUser.room_id == room_id
        ).all()

    # lol
    room.users = users
    return room


def _does_room_exist(session, room_id):
    return bool(session.query(count(Room.id)).filter(Room.id == room_id).scalar())

def _is_user_in_room(session, room_id, user_id):
    return bool(
        session.query(
            count(RoomUser.id)
        ).filter(
            RoomUser.user_id == user_id,
            RoomUser.room_id == room_id
        ).scalar()
    )


def join_queue(room_id, user_id):
    with db.session_context() as session:
        if not _is_user_in_room(session, room_id, user_id):
            raise UserNotInRoom()


def leave_queue(room_id, user_id):
    pass


def get_current_track(room_id):
    pass


def get_room_info(room_id):
    pass