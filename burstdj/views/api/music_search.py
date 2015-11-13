from apiclient.discovery import build

from cornice import Service


search_activity = Service(
    name='music_search',
    path='/api/music_search/{search_string}',
    permission='authenticated',
)


YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


@search_activity.get()
def get_search_activity(request):
    search_string = str(request.matchdict['search_string'])

    with open('./api_key') as api_file:
        api_key = api_file.read().rstrip('\n')

    youtube = build(
        YOUTUBE_API_SERVICE_NAME,
        YOUTUBE_API_VERSION,
        developerKey=api_key
    )

    return youtube.search().list(
        q=search_string,
        part="id,snippet",
        maxResults=15,
    ).execute()
