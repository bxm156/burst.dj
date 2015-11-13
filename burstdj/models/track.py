from enum import Enum

from sqlalchemy import Column
from sqlalchemy import Index
from sqlalchemy import Integer
from sqlalchemy.types import DateTime
from sqlalchemy.types import String
from sqlalchemy.sql.functions import now

from burstdj.models import Base
from burstdj.models import types


class TrackProvider(Enum):
    YOUTUBE = 1
    SOUNDCLOUD = 2


class Track(Base):
    __tablename__ = 'track'
    id = Column(Integer, primary_key=True, autoincrement=True)
    time_created = Column(DateTime, default=now())
    name = Column(String)
    provider = Column(Integer)
    track_provider_id = Column(String)
    length = Column(Integer)

Index('track_id', Track.provider, Track.track_provider_id, unique=True)