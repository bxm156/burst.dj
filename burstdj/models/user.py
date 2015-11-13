from sqlalchemy.sql.functions import now

from burstdj.models import *

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    time_created = Column(DateTime, default=now())
    name = Column(String)
    avatar_url = Column(String)
    #TODO: make this into a foreign key when we create the playlist table
    active_playlist_id = Column(Integer)
    playlists = relation("Playlist", backref="user")

Index('user_name', User.name, unique=True, mysql_length=255)
