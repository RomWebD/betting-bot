# models/match.py

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base


class Match(Base):
    __tablename__ = "matches"
    id = Column(Integer, primary_key=True, index=True)
    match_id = Column(String, unique=True, index=True)
    team1 = Column(String)
    team2 = Column(String)
    time = Column(String)
    score_team1 = Column(Integer)
    score_team2 = Column(Integer)
    period = Column(String)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    # Відношення до таблиці coefficients
    coefficients = relationship("Coefficient", back_populates="match")
