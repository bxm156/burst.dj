from collections import deque

from sqlalchemy.orm import joinedload
from sqlalchemy.orm.exc import NoResultFound

from burstdj.db import session_context
from burstdj.models.playlist import Playlist
from burstdj.models.track import Track


def create_playlist(user_id, name):
    playlist = Playlist(name=name, user_id=user_id, tracks=[])
    with session_context() as session:
        session.add(playlist)
    return playlist.id

def delete_playlist(user_id, playlist_id):
    with session_context() as session:
        playlist = _get_playlist(session, user_id, playlist_id)
        if playlist is None:
            return False
        session.delete(playlist)
    return True

def list_playlists(user_id):
    with session_context() as session:
        return session.query(Playlist).filter(Playlist.user_id==user_id).all()

def get_playlist(user_id, playlist_id):
    with session_context() as session:
        return _get_playlist(session, user_id, playlist_id)

def _get_playlist(session, user_id, playlist_id):
    try:
        playlist = session.query(Playlist).filter(
            Playlist.user_id==user_id,
            Playlist.id==playlist_id,
        ).one()
    except NoResultFound:
        return None
    return playlist

def add_track(user_id, playlist_id, track_id):
    with session_context() as session:
        try:
            track = session.query(Track).filter(Track.id==track_id).one()
        except NoResultFound:
            return False
        playlist = _get_playlist(session, user_id, playlist_id)
        if playlist is None:
            return False
        if track_id in playlist.tracks:
            return False
        playlist.tracks = playlist.tracks + [track_id]
    return True

def list_tracks(user_id, playlist_id):
    playlist = get_playlist(user_id, playlist_id)
    if playlist is None:
        return None
    if not playlist.tracks:
        return []
    with session_context() as session:
        tracks = session.query(Track).filter(
            Track.id.in_(playlist.tracks)
        ).all()
    available_track_ids = [t.id for t in tracks]
    track_queue = []
    # Order our tracks in our queue order
    for t_id in playlist.tracks:
        try:
            track_index = available_track_ids.index(t_id)
            track_queue.append(tracks[track_index])
        except ValueError:
            continue
    return track_queue

def next_track(user_id, playlist_id):
    # Gets the top track in the queue and rotates the queue
    with session_context() as session:
        playlist = _get_playlist(session, user_id, playlist_id)
        if playlist is None or not playlist.tracks:
            return None
        next_track_id = playlist.tracks[0]
        tracks = deque(playlist.tracks)
        tracks.rotate(-1)
        playlist.tracks = list(tracks)
        next_track = session.query(Track).filter(Track.id==next_track_id).one()
    return next_track
