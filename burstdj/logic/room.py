from burstdj import db
from burstdj.models.room import Room


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

def get_current_track(room_id):
    pass

def get_room_info(room_id):
    pass