import uuid
from datetime import datetime

from sqlalchemy import String, Integer, Boolean, ARRAY, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func

from .common import Base


class Sponsor(Base):
    __tablename__ = 'sponsors'

    user_id = mapped_column(UUID(as_uuid=True), nullable=False, primary_key=True, default=uuid.uuid4)
    extra_slots = mapped_column(Integer, nullable=False, default=0)
    ooc_color = mapped_column(String(6), nullable=True, default=None)
    allowed_markings = mapped_column(ARRAY(String), nullable=False, default=[])
    ghost_theme = mapped_column(String, nullable=True, default=None)
    have_sponsor_chat = mapped_column(Boolean, nullable=False, default=False)
    have_priority_join = mapped_column(Boolean, nullable=False, default=False)

    is_active = mapped_column(Boolean, nullable=False, default=False)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, user_id: uuid.UUID, ooc_color: str = None, allowed_markings: tuple[str] = None,
                 ghost_theme: str = None, have_sponsor_chat: bool = None, have_priority_join: bool = None,
                 is_active: bool = None, expiration_date: datetime = None):
        self.user_id = user_id
        self.ooc_color = ooc_color
        self.allowed_markings = allowed_markings
        self.ghost_theme = ghost_theme
        self.have_sponsor_chat = have_sponsor_chat
        self.have_priority_join = have_priority_join
        self.is_active = is_active
        self.expiration_date = expiration_date

    def __repr__(self):
        return f"<Sponsor(user_id={self.user_id}, ooc_color='{self.ooc_color}', " \
               f"allowed_markings={self.allowed_markings}, ghost_theme='{self.ghost_theme}', " \
               f"have_sponsor_chat='{self.have_sponsor_chat}', have_priority_join='{self.have_priority_join}', " \
               f"is_active='{self.is_active}')>"
