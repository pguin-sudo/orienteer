import uuid

from sqlalchemy import ForeignKey, Integer, String, BigInteger, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func

from .common import Base


class PromotionalCodeUsages(Base):
    __tablename__ = "promotional_code_usages"

    cache_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id = mapped_column(UUID(as_uuid=True), nullable=False)
    promotional_code = mapped_column(
        String, ForeignKey("promotional_codes.code"), nullable=False
    )

    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, user_id: uuid.UUID, promotional_code: str):
        self.user_id = user_id
        self.promotional_code = promotional_code

    def __repr__(self):
        return f"<PromotionalCodeUsages(cache_id={self.cache_id}, user_id={self.user_id}, promotional_code='{self.promotional_code}', created_at='{self.created_at}')>"
