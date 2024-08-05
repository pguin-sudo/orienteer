import datetime
import uuid

from sqlalchemy import Integer, UUID, ForeignKey, Interval
from sqlalchemy.orm import mapped_column

from .common import Base


class CachedPlaytime(Base):
    __tablename__ = 'seasons_cached_playtime'

    cached_playtime_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id = mapped_column(UUID(as_uuid=True), nullable=False)
    playtime = mapped_column(Interval, nullable=False)
    season_id = mapped_column(Integer, ForeignKey('seasons.season_id'), nullable=False)

    def __init__(self, user_id: uuid.UUID, playtime: datetime.timedelta, season_id: int):
        self.user_id = user_id
        self.playtime = playtime
        self.season_id = season_id

    def __repr__(self):
        return f"<CachedPlaytime(user_id={self.user_id}, playtime={self.playtime}, season_id={self.season_id})>"