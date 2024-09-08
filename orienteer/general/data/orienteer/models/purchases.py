from sqlalchemy import Integer, DateTime, UUID
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func

from .common import Base


class Purchase(Base):
    __tablename__ = "purchases"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    product_id = mapped_column(Integer, nullable=False)
    user_id = mapped_column(UUID(as_uuid=True), nullable=False)
    price = mapped_column(Integer, nullable=True)
    date = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    def __init__(self, product_id: int, user_id: UUID, price: price):
        self.product_id = product_id
        self.user_id = user_id
        self.price = price

    def __repr__(self):
        return (
            f"<Purchase(id={self.id}, product_id={self.product_id}, user_id={self.user_id}, "
            f"price={self.price}, date={self.date})>"
        )
