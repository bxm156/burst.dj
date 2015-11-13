from sqlalchemy import Column
from sqlalchemy import Index
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy.types import DateTime
from sqlalchemy.types import String
from sqlalchemy.sql.functions import now

from burstdj.models import Base
from burstdj.models import types

class UserTrackRating(Base):
    __tablename__ = 'user_track_rating'
    id = Column(Integer, primary_key=True, autoincrement=True)
    time_created = Column(DateTime, default=now())
    user_id = Column(Integer, ForeignKey("user.id"))
    track_id = Column(Integer, ForeignKey("track.id")) 
    rating = Column(Integer) # Average rating out of 10