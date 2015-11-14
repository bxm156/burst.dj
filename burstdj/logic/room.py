import datetime
import logging
import sys
import time
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql.functions import count

from burstdj import db
from burstdj.logic import track as track_logic
from burstdj.logic import playlist as playlist_logic
from burstdj.models.room import Room
from burstdj.models.room_queue import RoomQueue, RoomQueueLock
from burstdj.models.room_user import RoomUser
from burstdj.models.user import User


log = logging.getLogger('burstdj.room')


# for now we'll do this, but we'll want to tighten it
TRACK_FINISH_BUFFER = 2
TRACK_MAX_PLAYTIME = sys.maxint

QUEUE_LOCK_TIMEOUT = 5

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
            (count(RoomUser.user_id)),
        ).outerjoin(
            RoomUser
        ).group_by(
            Room
        ).order_by(
            desc(count(RoomUser.user_id)),
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
            RoomUser.user_id,
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
        RoomQueue.user_id,
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
            count(RoomUser.user_id)
        ).filter(
            RoomUser.user_id == user_id,
            RoomUser.room_id == room_id
        ).scalar()
    )

def _is_user_in_queue(session, room_id, user_id):
    return bool(
        session.query(
            count(RoomQueue.user_id)
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
    log_context = dict(action='join_queue', room_id=room_id, user_id=user_id)
    with db.session_context() as session:
        if not _is_user_in_room(session, room_id, user_id):
            log.info("user not in room %s", log_context)
            raise UserNotInRoom()

        try:
            _add_user_to_queue(session, room_id, user_id)
            log.info("added user to queue %s", log_context)
        except IntegrityError:
            session.rollback()
            log.info("user already in queue %s", log_context)
            return False

        return True


def leave_queue(room_id, user_id):
    log_context = dict(action='leave_queue', room_id=room_id, user_id=user_id)
    with db.session_context() as session:
        if not _does_room_exist(session, room_id):
            log.info("room does not exist %s", log_context)
            raise RoomNotFound()
        if not _is_user_in_room(session, room_id, user_id):
            log.info("user not in room %s", log_context)
            raise UserNotInRoom()

        rows_deleted = session.query(
            RoomQueue,
        ).filter(
            RoomQueue.user_id == user_id,
            RoomQueue.room_id == room_id,
        ).delete()

        log.info("removed user from queue %s", log_context)

        # TODO: skip current song if user is playing?

        return bool(rows_deleted)


def current_track(session, room):
    """Return the room's currently cached track, as long as it should still
    be playing.
    """
    if not room.current_track_id:
        return None

    log_context = dict(action='current_track', room_id=room.id, track_id=room.current_track_id)
    current_time = datetime.datetime.now()
    track = track_logic.load_track_by_id(session, room.current_track_id)
    if track is None:
        log.error("could not find track %s", log_context)
        return None

    log_context.update(dict(track_name=track.name))

    time_elapsed = current_time - room.time_track_started
    if time_elapsed.total_seconds() > TRACK_MAX_PLAYTIME:
        log.info("ending playback of track early due to time_elapsed:%s %s", time_elapsed, log_context)
        return None

    time_track_finished = room.time_track_started + datetime.timedelta(
        seconds=(track.length + TRACK_FINISH_BUFFER)
    )

    if current_time > time_track_finished:
        # track's done, so it's now stale
        log.info("track was done at time_track_finished:%s %s", time_track_finished, log_context)
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
        RoomQueue.user_id,
    ).first()


def _rotate_queue(session, room):
    """rotate current user to end of queue and return True.

    if there are no users, return False.
    """
    log_context = dict(action='rotate_queue', room_id=room.id)
    queue_entry = _first_queue_entry(session, room)
    if queue_entry is None:
        log.info("empty queue %s", log_context)
        return False

    user_id = queue_entry.user_id
    log.info("moving user:%s to end of queue %s", user_id, log_context)
    session.delete(queue_entry)
    session.flush()

    _add_user_to_queue(session, room.id, user_id)
    session.flush()

    return True


def choose_next_track(session, room):
    log_context = dict(action='choose_next_track', room_id=room.id)

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
        log.info("removing user:%s from queue due to no track %s", user_id, log_context)
        session.delete(queue_entry)
        session.flush()
        return choose_next_track(session, room)

    track.user_id = user_id
    return track


def acquire_queue_lock(room_id, user_id):
    """This is stupid.  We use integrity constraints on the RoomQueueLock
    table to enforce what is basically an application lock.

    Any request to /activity can trigger a queue update.  In that sense
    any request from a client is a potential "master."  This lock allows one
    of these  requests to obtain temporary ownership of the queue.

    In a real production system we'd use SELECT FOR UPDATE using innodb,
    or zookeeper, or something else entirely.  SQLite doesn't support
    SELECT FOR UPDATE.

    Will return True if lock was acquired; False if not.  Caller should
    wait a little before trying again, if it even has to try again.
    """
    log_context = dict(action='acquire_queue_lock', room_id=room_id, user_id=user_id)
    with db.session_context() as session:
        try:
            lock = RoomQueueLock(room_id=room_id)
            session.add(lock)
            session.flush()
            log.info("acquired - %s", log_context)
            return True  # we got it
        except IntegrityError:
            log.info("already locked - %s", log_context)
            session.rollback()

        lock = session.query(RoomQueueLock).filter(RoomQueueLock.room_id == room_id).first()
        if not lock:
            log.info("recently freed - %s", log_context)
            return False  # try again if we still need it

        current_time = datetime.datetime.now()
        if (current_time - lock.time_created).total_seconds() > QUEUE_LOCK_TIMEOUT:
            # assume the request that took the lock fucked up, and remove it
            session.query(RoomQueueLock).filter(RoomQueueLock.room_id == room_id).delete()
            log.info("deleted - %s", log_context)

        return False  # try again if we still need it


def release_queue_lock(room_id, user_id):
    log_context = dict(action='release_queue_lock', room_id=room_id, user_id=user_id)
    with db.session_context() as session:
        session.query(RoomQueueLock).filter(RoomQueueLock.room_id == room_id).delete()
        log.info("released - %s", log_context)


def assign_new_room_track(session, room, user_id):
    log_context = dict(action='assign_new_room_track', room_id=room.id, user_id=user_id)
    track = None
    queue_populated = _rotate_queue(session, room)
    if queue_populated:
        # can only get next track if queue is valid
        track = choose_next_track(session, room)
    if track:
        log.info("new track:%s user:%s %s %s", track.id, track.user_id, track.name, log_context)
        room.current_track_id = track.id
        room.current_user_id = track.user_id
        room.time_track_started = datetime.datetime.now()
    else:
        room.current_track_id = None
        room.current_user_id = None
        room.time_track_started = None
        log.info("no track %s", log_context)
    return track


def get_current_room_track(room_id, user_id):
    """
    Get the current track for the room.

    Note that this function can potentially change the room's current
    track, if the track is finished.

    :rtype: Track
    """
    log_context = dict(action='get_current_room_track', room_id=room_id, user_id=user_id)

    while True:
        with db.session_context() as session:
            room = _get_room(session, room_id)
            track = current_track(session, room)
            if track:
                log.info("same track:%s user:%s %s %s", track.id, room.current_user_id, track.name, log_context)
                room.track = track
                return room

        lock_acquired = False
        try:
            lock_acquired = acquire_queue_lock(room_id, user_id)
            if not lock_acquired:
                # someone else probably assigned the next song
                # so try our loop again.  this boots us back to
                # looking for the cached track for the room, so
                # we can hopefully avoid even entering this block again
                log.info("trying again %s", log_context)
                time.sleep(0.1)
                continue

            with db.session_context() as session:
                room = _get_room(session, room_id)
                track = assign_new_room_track(session, room, user_id)
        finally:
            if lock_acquired:
                release_queue_lock(room.id, user_id)

        room.track = track
        return room
