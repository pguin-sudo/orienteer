from sqlalchemy import Integer
from sqlalchemy.orm import mapped_column

from .common import Base


class SentBan(Base):
    __tablename__ = "sent_bans"

    id = mapped_column(Integer, primary_key=True)
    last_sent_ban_id = mapped_column(Integer)
    last_sent_role_ban_id = mapped_column(Integer)
