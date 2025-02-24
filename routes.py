from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from betting_utils import get_data_from_match

# , get_name_of_blocks
# from crud import add_blocks_to_db, add_markets_to_db
from database import get_db
from schemas import BlockCreate
from cache import cache

router = APIRouter()


@router.post("/add_blocks")
def add_block(block: BlockCreate, db: Session = Depends(get_db)):
    data = get_data_from_match(id=598606097)
    print(cache)
    new_block = ""
    # new_block = Block(col1=block.col1, col2=block.col2)
    # db.add(new_block)
    # db.commit()
    # db.refresh(new_block)
    return {"message": "Block added successfully", "block": new_block}
