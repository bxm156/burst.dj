from sqlalchemy import func
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Index
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy.orm import relation
from sqlalchemy.types import DateTime
from sqlalchemy.types import String

from burstdj.models import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    time_created = Column(DateTime, server_default=func.now())
    name = Column(String)
    avatar_url = Column(String)
    active_playlist_id = Column(Integer, ForeignKey("playlist.id"))
    playlists = relation("Playlist", backref="user")

Index('user_name', User.name, unique=True, mysql_length=255)
