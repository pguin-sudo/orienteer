from sqlalchemy import DateTime, Text, Integer, Boolean
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func

from .common import Base


class ChoosingPromo(Base):
    __tablename__ = "choosing_promo"  # Название таблицы в БД

    code = mapped_column(Text, primary_key=True, nullable=False)  # Промокод как PK
    youtuber = mapped_column(Text, nullable=False)  # Никнейм ютубера, который создал промокод
    usages = mapped_column(Integer, default=0)  # Количество успешных активаций (начинается с 0)
    end_time = mapped_column(DateTime(timezone=True), nullable=False)  # Время окончания действия промокода
    active = mapped_column(Boolean, default=True)  # Статус активности промокода

    def __init__(self, youtuber, code, end_time, active=True):
        self.youtuber = youtuber
        self.code = code
        self.end_time = end_time
        self.active = active

    def __repr__(self):
        return (
            f"<ChoosingPromo(code='{self.code}', youtuber='{self.youtuber}', "
            f"usages={self.usages}, end_time={self.end_time}, active={self.active})>"
        )
