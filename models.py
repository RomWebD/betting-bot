from sqlalchemy import Column, Integer, String
from database import Base


class Block(Base):
    __tablename__ = "blocks"
    id = Column(Integer, primary_key=True, index=True)
    block_id = Column(String, index=True)
    block_name = Column(String, index=True)


class Market(Base):
    __tablename__ = "markets"
    id = Column(Integer, primary_key=True, index=True)
    market_id = Column(String, index=True)
    market_name = Column(String, index=True)
