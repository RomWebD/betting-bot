import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from betting_utils import get_coefficients_from_match, get_list_of_match

# , get_name_of_blocks
# from crud import add_blocks_to_db, add_markets_to_db
from crud.matches import add_or_update_matches
from database import get_db
from schemas import BlockCreate
from cache import cache

router = APIRouter()


@router.post("/add_blocks")
def add_block(block: BlockCreate, db: Session = Depends(get_db)):
    now = datetime.datetime.now()
    print(now)
    matches = get_list_of_match()
    add_or_update_matches(matches)
    match_id = matches[0]["match_id"]
    coefficients = get_coefficients_from_match(match_id)
    print()
    new_block = ""
    # new_block = Block(col1=block.col1, col2=block.col2)
    # db.add(new_block)
    # db.commit()
    # db.refresh(new_block)
    return {"message": "Block added successfully", "block": new_block}
