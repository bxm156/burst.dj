from burstdj.models import *

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    time_created = Column(DateTime)
    name = Column(String)
    avatar_url = Column(String)
    #TODO: make this into a foreign key when we create the playlist table
    active_playlist_id = Column(Integer)

Index('user_name', User.name, unique=True, mysql_length=255)
