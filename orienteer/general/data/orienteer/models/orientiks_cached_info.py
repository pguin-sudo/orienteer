from sqlalchemy import Column, Integer, DateTime, func

from orienteer.general.data.orienteer.models.common import Base


class OrientiksCachedInfo(Base):
    __tablename__ = "orientiks_cached_infos"

    id = Column(Integer, primary_key=True, autoincrement=True)

    total_sponsorship = Column(Integer, default=0, nullable=False)
    total_friends = Column(Integer, default=0, nullable=False)
    total_pardons = Column(Integer, default=0, nullable=False)
    total_time_balancing = Column(Integer, default=0, nullable=False)
    total_spent = Column(Integer, default=0, nullable=False)
    total_fine = Column(Integer, default=0, nullable=False)
    total_from_time = Column(Integer, default=0, nullable=False)

    date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    def __init__(
        self,
        total_sponsorship=0,
        total_friends=0,
        total_pardons=0,
        total_time_balancing=0,
        total_spent=0,
        total_fine=0,
        total_from_time=0,
        date=None,
    ):
        self.total_sponsorship = total_sponsorship
        self.total_friends = total_friends
        self.total_pardons = total_pardons
        self.total_time_balancing = total_time_balancing
        self.total_spent = total_spent
        self.total_fine = total_fine
        self.total_from_time = total_from_time
        self.date = date or func.now()

    def __repr__(self):
        return (
            f"<OrientiksCachedInfo(id={self.id}, total_sponsorship={self.total_sponsorship}, "
            f"total_friends={self.total_friends}, total_pardons={self.total_pardons}, "
            f"total_time_balancing={self.total_time_balancing}, total_spent={self.total_spent}, "
            f"total_fine={self.total_fine}, total_from_time={self.total_from_time}, date={self.date})>"
        )
