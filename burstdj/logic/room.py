import datetime
import logging
import sys
from sqlalchemy import desc
from sqlalchemy.sql.functions import count

from burstdj import db
from burstdj.logic import track as track_logic
from burstdj.logic import playlist as playlist_logic
from burstdj.models.room import Room
from burstdj.models.room_queue import RoomQueue
from burstdj.models.room_user import RoomUser
from burstdj.models.user import User


log = logging.getLogger('burstdj.room')


# for now we'll do this, but we'll want to tighten it
TRACK_FINISH_BUFFER = 2
TRACK_MAX_PLAYTIME = sys.maxint

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


def list_room_users(room_id):
    with db.session_context() as session:
        return session.query(
            User
        ).join(
            RoomUser
        ).filter(
            RoomUser.room_id == room_id
        ).order_by(
            RoomUser.time_created,
            RoomUser.id,
        ).all()


def _query_room_djs(session, room_id):
    return session.query(
        User
    ).join(
        RoomQueue
    ).filter(
        RoomQueue.room_id == room_id
    ).order_by(
        RoomQueue.time_created,
        RoomQueue.id,
    )

def _list_room_djs(session, room_id):
    return _query_room_djs(session, room_id).all()

def list_room_djs(room_id):
    with db.session_context() as session:
        return _list_room_djs(session, room_id)

def get_room(room_id):
    with db.session_context() as session:
        return _get_room(session, room_id)

def _get_room(session, room_id, for_update=False):
    """

    :param session:
    :param room_id:
    :param for_update:
    :return:
    :rtype: Room
    """
    query = session.query(Room).filter(Room.id == room_id)
    if for_update:
        query = query.with_for_update()
    room = query.first()
    if room is None:
        raise RoomNotFound()
    return room

def join_room(room_id, user_id):
    with db.session_context() as session:
        if not _does_room_exist(session, room_id):
            raise RoomNotFound()

        if not _is_user_in_room(session, room_id, user_id):
            _leave_rooms(session, user_id)

            # join room
            room_user = RoomUser(
                room_id=room_id,
                user_id=user_id,
            )
            session.add(room_user)
            session.flush()

        room = session.query(Room).filter(Room.id == room_id).first()

    # lol
    room.users = list_room_users(room_id)
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

def _is_user_in_queue(session, room_id, user_id):
    return bool(
        session.query(
            count(RoomQueue.id)
        ).filter(
            RoomQueue.user_id == user_id,
            RoomQueue.room_id == room_id
        ).scalar()
    )

def _add_user_to_queue(session, room_id, user_id):
    room_queue = RoomQueue(
        room_id=room_id,
        user_id=user_id,
    )
    session.add(room_queue)
    session.flush()
    return room_queue

def join_queue(room_id, user_id):
    with db.session_context() as session:
        if not _does_room_exist(session, room_id):
            raise RoomNotFound()
        if not _is_user_in_room(session, room_id, user_id):
            raise UserNotInRoom()

        if _is_user_in_queue(session, room_id, user_id):
            return False

        _add_user_to_queue(session, room_id, user_id)
        return True


def leave_queue(room_id, user_id):
    with db.session_context() as session:
        if not _does_room_exist(session, room_id):
            raise RoomNotFound()
        if not _is_user_in_room(session, room_id, user_id):
            raise UserNotInRoom()

        rows_deleted = session.query(
            RoomQueue,
        ).filter(
            RoomQueue.user_id == user_id,
            RoomQueue.room_id == room_id,
        ).delete()

        return bool(rows_deleted)


def current_track(session, room):
    if not room.current_track_id:
        return None

    current_time = datetime.datetime.now()
    track = track_logic.load_track_by_id(session, room.current_track_id)

    time_elapsed = current_time - room.time_track_started
    if time_elapsed.total_seconds() > TRACK_MAX_PLAYTIME:
        log.info("ending playback of track %s early due to time_elapsed:%s", track.name, time_elapsed)
        return None

    time_track_finished = room.time_track_started + datetime.timedelta(
        seconds=(track.length + TRACK_FINISH_BUFFER)
    )

    if current_time > time_track_finished:
        # track's done, so it's now stale
        log.info("track %s is done", track.name)
        return None

    return track


def _first_queue_entry(session, room):
    """
    :rtype: RoomQueue
    """
    return session.query(
        RoomQueue
    ).filter(
        RoomQueue.room_id == room.id
    ).order_by(
        RoomQueue.time_created,
        RoomQueue.id,
    ).first()


def _rotate_queue(session, room):
    """rotate current user to end of queue and return True.

    if there are no users, return False.
    """
    queue_entry = _first_queue_entry(session, room)
    if queue_entry is None:
        log.info("rotate_queue: empty")
        return False

    user_id = queue_entry.user_id
    log.info("rotate_queue: moving user:%s to end of queue", user_id)
    session.delete(queue_entry)
    session.flush()

    _add_user_to_queue(session, room.id, user_id)
    session.flush()

    return True


def choose_next_track(session, room):
    # pick next user from queue
    # TODO: check that user's last ping is decent
    queue_entry = _first_queue_entry(session, room)
    if queue_entry is None:
        return None

    user_id = queue_entry.user_id
    playlist_id = playlist_logic._get_user_active_playlist_id(session, user_id)
    track = playlist_logic._get_next_track(session, user_id, playlist_id)
    if track is None:
        # this guy has no right to be DJing
        log.info("removing user:%s from queue due to no track", user_id)
        session.delete(queue_entry)
        session.flush()
        return choose_next_track(session, room)

    track.user_id = user_id
    return track


def get_current_room_track(room_id):
    """
    :rtype: Track
    """
    with db.session_context() as session:
        room = _get_room(session, room_id, for_update=True)
        track = current_track(session, room)
        if track:
            log.info("get_current_room_track: same track %s", track.name)
        else:
            queue_populated = _rotate_queue(session, room)
            if queue_populated:
                # can only get next track if queue is valid
                track = choose_next_track(session, room)
            if track:
                log.info("get_current_room_track: new track %s, user %s", track.name, track.user_id)
                room.current_track_id = track.id
                room.current_user_id = track.user_id
                room.time_track_started = datetime.datetime.now()
            else:
                room.current_track_id = None
                room.current_user_id = None
                room.time_track_started = None
                log.info("get_current_room_track: no track")

    room.track = track
    return room
