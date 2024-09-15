import enum

from sqlalchemy import String, Integer, Boolean, Enum, DateTime, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func

from .common import Base


class TransactionType(enum.Enum):
    Spend = "Spend"
    Ban = "Ban"
    Pardon = "Pardon"
    Transfer = "Transfer"
    Promo = "Promo"
    Boosty = "Boosty"
    Tip = "Tip"
    Playtime = "Playtime"
    Other = "Other"


class Transaction(Base):
    __tablename__ = "transactions"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id = mapped_column(UUID(as_uuid=True), nullable=False)
    name = mapped_column(String, nullable=False)
    transaction_type = mapped_column(Enum(TransactionType), nullable=False)
    amount = mapped_column(Float, nullable=False)

    is_active = mapped_column(Boolean, nullable=False, default=True)
    time = mapped_column(DateTime(timezone=True), server_default=func.now())

    def __init__(
        self, user_id, name, transaction_type, amount, is_active=None, time=None
    ):
        self.user_id = user_id
        self.name = name
        self.transaction_type = transaction_type
        self.amount = amount
        self.is_active = is_active
        self.time = time
