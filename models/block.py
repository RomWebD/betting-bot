from sqlalchemy import Column, Integer, String
from database import Base


class Block(Base):
    __tablename__ = "blocks"
    id = Column(Integer, primary_key=True, index=True)
    block_id = Column(String, unique=True, index=True)
    block_name = Column(String, index=True)
