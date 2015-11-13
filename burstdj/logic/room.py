from sqlalchemy import desc
from sqlalchemy.sql.functions import count

from burstdj import db
from burstdj.models.room import Room
from burstdj.models.room_user import RoomUser


class RoomAlreadyExists(Exception):
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


def get_current_track(room_id):
    pass


def get_room_info(room_id):
    pass