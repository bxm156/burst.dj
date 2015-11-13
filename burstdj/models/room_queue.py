from burstdj.models import *
from burstdj.models.room import Room
from burstdj.models.user import User

class RoomQueue(Base):
    __tablename__ = 'room_queue'
    id = Column(Integer, primary_key=True)
    time_created = Column(DateTime)
    room_id = Column(Integer, ForeignKey(Room.id))
    user_id = Column(Integer, ForeignKey(User.id))
