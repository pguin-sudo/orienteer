from sqlalchemy import Column, Integer, DateTime, String, ARRAY, JSON

from .common import Base


class Season(Base):
    __tablename__ = 'seasons'

    season_id = Column(Integer, primary_key=True, autoincrement=True)
    start_date = Column(DateTime, nullable=False)
    title = Column(String(256), nullable=False)
    description = Column(String, nullable=False)
    color = Column(String(6), nullable=False)
    image_url = Column(String, nullable=False)
    awards = Column(ARRAY(Integer), nullable=False)

    def __init__(self, start_date, title, description, color, image_url, awards):
        self.start_date = start_date
        self.title = title
        self.description = description
        self.color = color
        self.image_url = image_url
        self.awards = awards

    def __repr__(self):
        return f"<Season(season_id={self.season_id}, title='{self.title}', start_date={self.start_date}, color='{self.color}')>"
