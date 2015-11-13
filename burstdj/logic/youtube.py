import isodate
from apiclient.discovery import build


YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


def load_api_key():
    with open('./api_key') as api_file:
        return api_file.read().rstrip('\n')


def get_client():
    api_key = load_api_key()
    return build(
        YOUTUBE_API_SERVICE_NAME,
        YOUTUBE_API_VERSION,
        developerKey=api_key
    )


def search(query, limit=15):
    youtube = get_client()
    return youtube.search().list(
        q=query,
        part="id,snippet",
        maxResults=limit,
    ).execute()


def video_info(id):
    youtube = get_client()
    result = youtube.videos().list(
        id=id,
        part="id,snippet,contentDetails",
        maxResults=1,
    ).execute()
    items = result['items']
    if not items:
        return None
    item = items[0]

    # FFS
    duration_str = item['contentDetails']['duration']
    duration = isodate.parse_duration(duration_str)
    # that shitty function won't give us a timedelta if duration had months or years
    # and this will crash lol
    length = duration.total_seconds()

    return dict(
        id=item['id'],
        thumbnail=item['snippet']['thumbnails']['default'],
        title=item['snippet']['title'],
        duration=duration_str,
        length=length,
    )
