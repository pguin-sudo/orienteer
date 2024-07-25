from sqlalchemy import Column, Integer, String, UUID

from .common import Base


class Orientiks(Base):
    __tablename__ = 'orientiks'

    user_id = Column(UUID(as_uuid=True), primary_key=True,
                     nullable=False)
    sponsorship = Column(Integer, default=0)
    friends = Column(Integer, default=0)
    pardons = Column(Integer, default=0)
    time_balancing = Column(Integer, default=0)
    spent = Column(Integer, default=0)

    def __init__(self, user_id, sponsorship=0, friends=0, pardons=0, time_balancing=0, spent=0):
        self.user_id = user_id
        self.sponsorship = sponsorship
        self.friends = friends
        self.pardons = pardons
        self.time_balancing = time_balancing
        self.spent = spent

    def __repr__(self):
        return f"<Orientiks(user_id={self.user_id}, sponsorship={self.sponsorship}, " \
            f"friends={self.friends}, pardons={self.pardons}, time_balancing={self.time_balancing}, " \
            f"spent={self.spent})>"
