from burstdj.models import *

class Room(Base):
    __tablename__ = 'room'
    id = Column(Integer, primary_key=True)
    time_created = Column(DateTime)
    name = Column(String)
    current_user_id = Column(Integer, ForeignKey("user.id"))
    #TODO: Make a ForeignKey when we get track models implemented
    current_track_id = Column(Integer)
    time_track_started = Column(DateTime)

    #TODO: Include if we have extra time
    #admin_user_id = Column(Integer)
