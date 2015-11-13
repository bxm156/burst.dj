from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Index
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy.orm import relation
from sqlalchemy.types import DateTime
from sqlalchemy.types import String
from sqlalchemy.sql.functions import now

from burstdj.models import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    time_created = Column(DateTime, default=now())
    name = Column(String)
    avatar_url = Column(String)
    active_playlist_id = Column(Integer, ForeignKey("playlist.id"))

Index('user_name', User.name, unique=True, mysql_length=255)
