from sqlalchemy import Column, Integer, String
from database import Base


class Market(Base):
    __tablename__ = "markets"
    id = Column(Integer, primary_key=True, index=True)
    market_id = Column(String, unique=True, index=True)
    market_name = Column(String, index=True)
