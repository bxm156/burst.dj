import time

from burstdj.models.track import Track
from burstdj.models.user_track_rating import UserTrackRating
from burstdj.logic.playlist import get_user
from burstdj.db import session_context
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import func




def load_track_by_id(session, track_id):
    """
    :rtype: Track
    """
    return session.query(Track).filter(Track.id == track_id).first()


def serialize_track(track, time_started=None):
    if track is None:
        return None

    time_started = None if time_started is None else time.mktime(time_started.timetuple())
    return dict(
        id=track.id,
        name=track.name,
        provider_track_id=track.provider_track_id,
        provider=track.provider,
        time_started=time_started,
        length=track.length,
        average_rating=track.average_rating,
    )


def serialize_tracks(tracks):
    return [serialize_track(track) for track in tracks]


def rate_track(user_id, track_id, rating):
    try:
        user = get_user(user_id)
    except:
        return False
    with session_context() as session:
        track = load_track_by_id(session, track_id)
        if track is None:
            return False
        rating = int(rating)
        if rating > 10:
            rating = 10
        if rating < 2:
            rating = 2
        try:
            current_rating = session.query(UserTrackRating).filter(
                UserTrackRating.user_id==user_id,
                UserTrackRating.track_id==track_id,
            ).one()
        except NoResultFound:
            current_rating = UserTrackRating(
                user_id=user_id,
                track_id=track_id,
            )

        current_rating.rating = rating
        session.add(current_rating)
    return update_average_rating(track_id)

def update_average_rating(track_id):
    with session_context() as session:
        track = load_track_by_id(session, track_id)
        if track is None:
            return False
        average = session.query(
            func.avg(UserTrackRating.rating)
        ).filter(
            UserTrackRating.track_id==track_id,
        ).first()[0]
        if average is None:
            return False
        track.average_rating = int(round(average))
    return track.average_rating





