from sqlalchemy import JSON, Integer, DateTime, String, Boolean
from sqlalchemy.orm import mapped_column

from .common import Base


class PromotionalCode(Base):
    __tablename__ = "promotional_codes"

    code = mapped_column(String, nullable=False, primary_key=True)
    usages = mapped_column(Integer, nullable=False, default=10000)
    jobs = mapped_column(JSON, nullable=False, default={})
    dependencies = mapped_column(JSON, nullable=False, default={})
    expiration_date = mapped_column(DateTime(timezone=True), nullable=True)
    is_creator = mapped_column(Boolean, nullable=False, default=False)

    def __init__(
        self,
        code,
        usages=None,
        jobs=None,
        dependencies=None,
        expiration_date=None,
        is_creator=None,
    ):
        self.code = code
        self.usages = usages
        self.jobs = jobs
        self.dependencies = dependencies
        self.expiration_date = expiration_date
        self.is_creator = is_creator

    def __repr__(self):
        return (
            f"<PromotionalCodes(code='{self.code}', usages={self.usages}, "
            f"jobs={self.jobs}, dependencies={self.dependencies}, "
            f"expiration_date={self.expiration_date}, is_creator={self.is_creator})>"
        )
