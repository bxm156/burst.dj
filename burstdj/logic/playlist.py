from sqlalchemy.orm.exc import NoResultFound

from burstdj.db import session_context
from burstdj.models.playlist import Playlist

def create_playlist(user_id, name):
    playlist = Playlist(name=name, user_id=user_id, tracks=[])
    with session_context() as session:
        session.add(playlist)
    return playlist.id

def delete_playlist(playlist_id):
    with session_context() as session:
        try:
            playlist = session.query(Playlist).filter(Playlist.id==playlist_id).one()
        except NoResultFound:
            return False
        session.delete(playlist)
    return True