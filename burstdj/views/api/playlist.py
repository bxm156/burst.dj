from cornice import Service
from burstdj.core.error import HTTPBadRequest, HTTPConflict, HTTPNotFound
from burstdj.logic import security
from burstdj.logic import playlist as playlist_logic
from burstdj.logic import track as track_logic
from burstdj.logic.playlist import TrackNotFound

playlists = Service(
    name='playlists',
    path='/api/user/{user_id}/playlist',
    permission='authenticated',
)

add_track = Service(
    name='add_track',
    path='/api/user/{user_id}/playlist/{playlist_id}/add_track',
    permission='authenticated',
)

playlist = Service(
    name='playlist',
    path='/api/user/{user_id}/playlist/{playlist_id}',
    permission='authenticated',
)

active_playlist = Service(
    name='active_playlist',
    path='/api/user/{user_id}/active_playlist',
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
        id=playlist_id,
        name=name,
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
    return dict(
        id=playlist.id,
        name=playlist.name,
        tracks=track_logic.serialize_tracks(tracks),
    )

@active_playlist.get()
def get_active_playlist(request):
    """Shows active playlist id for a user
    """
    user_id = request.matchdict['user_id']

    user = playlist_logic.get_user(user_id)
    playlist = playlist_logic.get_playlist(user_id, user.active_playlist_id)
    if playlist is None:
        return None

    tracks = playlist_logic.list_tracks(user_id, playlist.id)
    tracks_info = [
        dict(
            id=track.id,
            name=track.name,
        )
        for track in tracks
    ]
    return dict(
        id=playlist.id,
        name=playlist.name,
        tracks=tracks_info,
    )

@active_playlist.post()
def set_active_playlist(request):
    """Set the active playlist id for a user
    """
    user_id = request.matchdict['user_id']
    playlist_id = request.json_body.get('playlist_id', None)

    success = playlist_logic.set_user_active_playlist(user_id, playlist_id)
    if not success:
        raise HTTPNotFound()
        
    return dict(
        success=True,
    )

@add_track.post()
def add_track_to_playlist(request):
    """Adds a track to a playlist
    """
    user_id = request.matchdict['user_id']
    playlist_id = request.matchdict['playlist_id']

    provider = request.json_body.get('provider', None)
    provider_track_id = request.json_body.get('provider_track_id', None)

    if (
        provider is None or
        provider_track_id is None
    ):
        raise HTTPBadRequest()

    try:
        success = playlist_logic.add_track(
            user_id,
            playlist_id,
            provider,
            provider_track_id,
        )
    except TrackNotFound:
        raise HTTPBadRequest()

    return dict(success=success)
