from burstdj.models.track import Track


def load_track_by_id(session, track_id):
    """
    :rtype: Track
    """
    return session.query(Track).filter(Track.id == track_id).first()
