from burstdj.models.track import Track


def load_track_by_id(session, track_id):
    """
    :rtype: Track
    """
    return session.query(Track).filter(Track.id == track_id).first()


def serialize_track(track, time_started=None):
    if track is None:
        return None
    time_started = None if time_started is None else time_started.isoformat()
    return dict(
        id=track.id,
        name=track.name,
        provider_track_id=track.provider_track_id,
        provider=track.provider,
        time_started=time_started,
        length=track.length,
    )


def serialize_tracks(tracks):
    return [serialize_track(track) for track in tracks]