from burstdj.models import *
from burstdj.models.user import User
from burstdj.models import types

class Playlist(Base):
    __tablename__ = 'playlist'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    user_id = Column(Integer, ForeignKey("%s.id" % User.__tablename__))
    tracks = Column(types.JSONEncoded)