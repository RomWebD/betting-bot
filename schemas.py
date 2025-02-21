from pydantic import BaseModel

class BlockCreate(BaseModel):
    block_id: str
    block_name: str