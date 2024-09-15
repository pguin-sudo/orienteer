from sqlalchemy import BigInteger, Float
from sqlalchemy.orm import mapped_column

from .common import Base


class RoleTimeCoefficient(Base):
    __tablename__ = "role_time_coefficients"

    role_id = mapped_column(BigInteger, primary_key=True)
    coefficient = mapped_column(Float, nullable=False)
