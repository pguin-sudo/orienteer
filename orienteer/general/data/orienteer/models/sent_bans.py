from sqlalchemy import Column, Integer

from .common import Base


class SentBan(Base):
    __tablename__ = 'sent_bans'

    id = Column(Integer, primary_key=True)
    last_sent_ban_id = Column(Integer)
    last_sent_role_ban_id = Column(Integer)