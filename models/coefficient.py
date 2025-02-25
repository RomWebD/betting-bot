from sqlalchemy import Column, Integer, String, JSON, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base


class Coefficient(Base):
    __tablename__ = "coefficients"
    id = Column(Integer, primary_key=True, index=True)
    match_id = Column(String, ForeignKey("matches.match_id"), index=True)
    block_id = Column(String, ForeignKey("blocks.block_id"), index=True)
    market_id = Column(String, ForeignKey("markets.market_id"), index=True)
    values = Column(JSON)  # Зберігаємо масив коефіцієнтів в JSON
    score1 = Column(Integer, default=0)  # Рахунок команди 1
    score2 = Column(Integer, default=0)  # Рахунок команди 2
    period = Column(String, default="")  # Період гри (наприклад, 1-й тайм, 2-й тайм)
    cps = Column(String)  # Current Period Status
    add_info = Column(String)
    time = Column(String, default="")  # Час у форматі MM:SS
    # timestamp = Column(DateTime(timezone=True), server_default=func.now())

    # Відношення до інших таблиць
    match = relationship("Match", back_populates="coefficients")
    block = relationship("Block")
    market = relationship("Market")
