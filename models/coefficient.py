from sqlalchemy import Column, Integer, String, JSON,  ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base


class Coefficient(Base):
    __tablename__ = "coefficients"
    id = Column(Integer, primary_key=True, index=True)
    match_id = Column(String, ForeignKey("matches.match_id"), index=True)
    values = Column(JSON)  # Зберігаємо масив коефіцієнтів в JSON
    score1 = Column(String, default="0")  # Рахунок команди 1
    score2 = Column(String, default="0")  # Рахунок команди 2
    cp = Column(String, default="")  # Період гри (наприклад, 1-й тайм, 2-й тайм)
    period = Column(String, default="")  # Період гри (наприклад, 1-й тайм, 2-й тайм)
    quarter_account = Column(JSON)
    time = Column(String, default="")  # Час у форматі MM:SS
    # timestamp = Column(DateTime(timezone=True), server_default=func.now())

    # Відношення до інших таблиць
    match = relationship("Match", back_populates="coefficients")
