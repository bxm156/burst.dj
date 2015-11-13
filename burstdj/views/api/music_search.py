from cornice import Service

from burstdj.logic import youtube

search_activity = Service(
    name='music_search',
    path='/api/music_search/{search_string}',
    permission='authenticated',
)

track_info = Service(
    name='track_info',
    path='/api/track_info/{provider}/{provider_track_id}',
    permission='authenticated',
)


@search_activity.get()
def get_search_activity(request):
    search_string = str(request.matchdict['search_string'])
    limit = request.params.get('limit', 15)
    return youtube.search(search_string, limit=limit)


@track_info.get()
def get_track_info(request):
    provider = str(request.matchdict['provider'])
    provider_track_id = str(request.matchdict['provider_track_id'])
    return youtube.video_info(provider_track_id)