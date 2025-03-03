# models/match.py

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base


class Match(Base):
    __tablename__ = "matches"
    id = Column(Integer, primary_key=True, index=True)
    match_id = Column(String, unique=True, index=True)
    league = Column(String)
    team1 = Column(String)
    team2 = Column(String)

    # Статуси матчі
    status = Column(String, default="scheduled")
    # scheduled — матч планується,
    # live — матч в процесі
    # finished — матч завершився

    curr_period_quarter = Column(String)
    additional_info = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Відношення до таблиці coefficients
    coefficients = relationship("Coefficient", back_populates="match")
