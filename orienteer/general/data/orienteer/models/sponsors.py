import uuid
from sqlalchemy import Column, String, Integer, Boolean, ARRAY
from sqlalchemy.dialects.postgresql import UUID

from .common import Base


class Sponsor(Base):
    __tablename__ = 'sponsors'

    user_id = Column(UUID(as_uuid=True), nullable=False,
                     primary_key=True, default=uuid.uuid4)
    extra_slots = Column(Integer, nullable=False, default=0)
    ooc_color = Column(String, nullable=False, default='87cefa')
    allowed_markings = Column(ARRAY(String), nullable=False, default=[])
    ghost_theme = Column(String, nullable=False, default='')
    have_sponsor_chat = Column(Boolean, nullable=False, default=False)
    have_priority_join = Column(Boolean, nullable=False, default=False)
    is_active = Column(Boolean, nullable=False, default=False)

    def __init__(self, user_id: uuid.UUID, ooc_color: str = None, allowed_markings: tuple[str] = None, ghost_theme: str = None, have_sponsor_chat: bool = None, have_priority_join: bool = None, is_active: bool = None):
        self.user_id = user_id
        self.ooc_color = ooc_color
        self.allowed_markings = allowed_markings
        self.ghost_theme = ghost_theme
        self.have_sponsor_chat = have_sponsor_chat
        self.have_priority_join = have_priority_join
        self.is_active = is_active

    def __repr__(self):
        return f"<Sponsor(user_id={self.user_id}, ooc_color='{self.ooc_color}', " \
            f"allowed_markings={self.allowed_markings}, ghost_theme='{self.ghost_theme}', " \
            f"have_sponsor_chat='{self.have_sponsor_chat}', have_priority_join='{self.have_priority_join}', " \
            f"is_active='{self.is_active}')>"
