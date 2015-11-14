from sqlalchemy.sql.functions import now

from burstdj.models import *
from burstdj.models.room import Room
from burstdj.models.user import User


class RoomQueue(Base):
    __tablename__ = 'room_queue'
    time_created = Column(DateTime, default=now())
    room_id = Column(Integer, ForeignKey(Room.id), primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id), primary_key=True)


class RoomQueueLock(Base):
    """This is stupid.  We use integrity constraints on this table
    to enforce what is basically an application lock.

    Any request to /activity can trigger a queue update.  In that sense
    any request from a client is a potential "master."  This lock allows one
    of these  requests to obtain temporary ownership of the queue.

    In a real production system we'd use SELECT FOR UPDATE using innodb,
    or zookeeper, or something else entirely.  SQLite doesn't support
    SELECT FOR UPDATE.
    """
    __tablename__ = 'room_queue_lock'
    time_created = Column(DateTime, default=now())
    room_id = Column(Integer, ForeignKey(Room.id), primary_key=True)
