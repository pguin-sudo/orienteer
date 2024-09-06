import uuid

from sqlalchemy import String, Integer, Boolean, ARRAY, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func

from .common import Base


class Sponsor(Base):
    __tablename__ = 'sponsors'

    user_id = mapped_column(UUID(as_uuid=True), nullable=False, primary_key=True, default=uuid.uuid4)
    ooc_color = mapped_column(String(6), nullable=True, default=None)
    priority_join = mapped_column(Boolean, nullable=False, default=False)
    extra_slots = mapped_column(Integer, nullable=False, default=0)
    allowed_markings = mapped_column(ARRAY(String), nullable=False, default=[])
    loadouts = mapped_column(ARRAY(String), nullable=False, default=[])
    open_all_roles = mapped_column(Boolean, nullable=False, default=False)
    ghost_theme = mapped_column(String, nullable=True, default=False)

    sponsor_chat = mapped_column(Boolean, nullable=False, default=False)

    is_active = mapped_column(Boolean, nullable=False, default=True)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
