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
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    # Відношення до інших таблиць
    match = relationship("Match", back_populates="coefficients")
    block = relationship("Block")
    market = relationship("Market")
