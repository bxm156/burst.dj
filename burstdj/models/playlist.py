from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Index
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy.orm import relation
from sqlalchemy.sql.functions import now
from sqlalchemy.types import DateTime
from sqlalchemy.types import String

from burstdj.models import Base
from burstdj.models import types
from burstdj.models.user import User


class Playlist(Base):
    __tablename__ = 'playlist'
    id = Column(Integer, primary_key=True, autoincrement=True)
    time_created = Column(DateTime, default=now())
    name = Column(String)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relation("User", backref="playlists", foreign_keys=[user_id])
    tracks = Column(types.JSONValue)