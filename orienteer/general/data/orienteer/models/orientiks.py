from sqlalchemy import Integer, UUID
from sqlalchemy.orm import mapped_column

from .common import Base


class Orientiks(Base):
    __tablename__ = 'orientiks'

    user_id = mapped_column(UUID(as_uuid=True), primary_key=True, nullable=False)
    sponsorship = mapped_column(Integer, default=0, nullable=False)
    friends = mapped_column(Integer, default=0, nullable=False)
    pardons = mapped_column(Integer, default=0, nullable=False)
    time_balancing = mapped_column(Integer, default=0, nullable=False)
    spent = mapped_column(Integer, default=0, nullable=False)

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
