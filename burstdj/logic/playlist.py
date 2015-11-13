from collections import deque

from sqlalchemy.orm import joinedload
from sqlalchemy.orm.exc import NoResultFound

from burstdj.db import session_context
from burstdj.models.playlist import Playlist
from burstdj.models.track import Track
from burstdj.models.user import User


def get_user(user_id):
    with session_context() as session:
        user = session.query(User).filter(User.id==user_id).one()
    return user

def set_user_active_playlist(user_id, playlist_id):
    with session_context() as session:
        user = session.query(User).filter(User.id==user_id).one()
        playlist = _get_playlist(session, user_id, playlist_id)
        if playlist is None:
            return False
        user.active_playlist_id = playlist_id
    return True

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

def add_track(user_id, playlist_id, name, provider, track_provider_id, length_in_seconds):
    track_id = _load_or_create_track(name, provider,track_provider_id, length_in_seconds)
    with session_context() as session:
        playlist = _get_playlist(session, user_id, playlist_id)
        if playlist is None:
            return False
        if track_id in playlist.tracks:
            return False
        playlist.tracks = playlist.tracks + [track_id]
    return True

def remove_track(user_id, playlist_id, track_id):
    with session_context() as session:
        playlist = _get_playlist(session, user_id, playlist_id)
        if track_id not in playlist.tracks:
            return False
        track_index = playlist.tracks.index(track_id)
        playlist.tracks = playlist.tracks[:track_index] + playlist.tracks[track_index + 1:]
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

def get_next_track(user_id, playlist_id):
    # Gets the top track in the queue and rotates the queue
    with session_context() as session:
        playlist = _get_playlist(session, user_id, playlist_id)
        if playlist is None or not playlist.tracks:
            return None
        next_track_id = playlist.tracks[0]
        tracks = deque(playlist.tracks)
        tracks.rotate(-1)
        playlist.tracks = list(tracks)
        next_track = _load_track(session, next_track_id)
    # Bunk track data, clean it up and get next track
    if next_track is None:
        remove_track(user_id, playlist_id, next_track_id)
        return get_next_track(user_id, playlist_id)
    return next_track

def _load_track(session, track_id):
    try:
        track = session.query(Track).filter(Track.id==track_id).one()
    except NoResultFound:
        return None
    return track

def _load_or_create_track(name, provider, track_provider_id, length_in_seconds):
    with session_context() as session:
        try:
            track = session.query(Track).filter(
                Track.provider == provider,
                Track.track_provider_id == track_provider_id,
            ).one()
        except NoResultFound:
            track = Track(
                name=name,
                provider=provider,
                track_provider_id=track_provider_id,
                length=length
            )
            session.add(track)
    return track.id


