from cornice import Service
from burstdj.core.error import HTTPBadRequest, HTTPConflict

from burstdj.logic import security
from burstdj.logic import playlist as playlist_logic

playlists = Service(
    name='playlist',
    path='/api/user/{user_id}/playlist',
    permission='authenticated',
)

playlist = Service(
    name='playlist',
    path='/api/user/{user_id}/playlist/{playlist_id}',
    permission='authenticated',
)

@playlists.post()
def create_playlist(request):
    """Create a playlist for the user and return its id
    """
    user_id = request.matchdict['user_id']

    name = request.json_body.get('name', None)

    if name is None:
        raise HTTPBadRequest()

    playlist_id = playlist_logic.create_playlist(user_id, name)

    return dict(
        playlist_id=playlist_id,
    )

@playlists.get()
def list_playlists(request):
    """Lists all playlists for the user
    """
    user_id = request.matchdict['user_id']

    playlists = playlist_logic.list_playlists(user_id)

    return [
        dict(
            id=plist.id,
            name=plist.name,
            num_tracks=len(plist.tracks),
        )
        for plist in playlists
    ]

@playlist.get()
def get_playlist(request):
    """Shows playlist name and all tracks
    """
    user_id = request.matchdict['user_id']
    playlist_id = request.matchdict['playlist_id']

    playlist = playlist_logic.get_playlist(user_id, playlist_id)
    if not playlist:
        return None
    tracks = playlist_logic.list_tracks(user_id, playlist_id)
    tracks_info = [
        dict(
            id=track.id,
            name=track.name,
            artist=track.artist,
        )
        for track in tracks
    ]
    return dict(
        id=playlist.id,
        name=playlist.name,
        tracks=tracks_info,
    )








