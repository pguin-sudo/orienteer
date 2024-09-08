from sqlalchemy import Integer, DateTime, String, ARRAY
from sqlalchemy.orm import mapped_column

from .common import Base


class Season(Base):
    __tablename__ = "seasons"

    season_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    start_date = mapped_column(DateTime(timezone=True), nullable=False)
    title = mapped_column(String(256), nullable=False)
    description = mapped_column(String, nullable=False)
    color = mapped_column(String(6), nullable=False)
    image_url = mapped_column(String, nullable=False)
    awards = mapped_column(ARRAY(Integer), nullable=False)

    def __init__(self, start_date, title, description, color, image_url, awards):
        self.start_date = start_date
        self.title = title
        self.description = description
        self.color = color
        self.image_url = image_url
        self.awards = awards

    def __repr__(self):
        return f"<Season(season_id={self.season_id}, title='{self.title}', start_date={self.start_date}, color='{self.color}')>"
