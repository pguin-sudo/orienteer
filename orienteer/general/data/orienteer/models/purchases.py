from sqlalchemy import Column, Integer, DateTime, UUID
from sqlalchemy.sql import func

from .common import Base


class Purchase(Base):
    __tablename__ = 'purchases'

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, nullable=False)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    price = Column(Integer, nullable=False)
    date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    def __repr__(self):
        return f"<Purchase(id={self.id}, product_id={self.product_id}, user_id={self.user_id}, " \
               f"price={self.price}, date={self.date})>"

