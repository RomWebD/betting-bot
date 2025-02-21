import json
from sqlalchemy.orm import Session
from models import Block, Market
from database import SessionLocal


# Додавання нових блоків
def add_blocks_to_db(db: Session, blocks_list):
    # Перевіряємо існуючі записи, щоб не було дублікатів
    existing_block_ids = set(
        [block.block_id for block in db.query(Block.block_id).all()]
    )

    # Створюємо нові об'єкти, яких ще немає в БД
    new_blocks = [
        Block(block_id=item["block_id"], block_name=item["block_name"])
        for item in blocks_list
        if item["block_id"] not in existing_block_ids
    ]

    # Bulk insert нових записів
    db.bulk_save_objects(new_blocks)
    db.commit()


# Додавання нових маркетів
def add_markets_to_db(db: Session, market_list):
    # Перевіряємо існуючі записи
    existing_market_ids = set(
        [market.market_id for market in db.query(Market.market_id).all()]
    )

    # Створюємо нові об'єкти
    new_markets = [
        Market(market_id=item["market_id"], market_name=item["market_name"])
        for item in market_list
        if item["market_id"] not in existing_market_ids
    ]

    # Bulk insert нових записів
    db.bulk_save_objects(new_markets)
    db.commit()


def load_blocks_from_db():
    db = SessionLocal()
    blocks = db.query(Block).all()
    blocks_list = [
        {"block_id": block.block_id, "block_name": block.block_name} for block in blocks
    ]
    db.close()

    # Збереження в JSON
    with open("data/blocks.json", "w") as f:
        json.dump(blocks_list, f)


def load_markets_from_db():
    db = SessionLocal()
    blocks = db.query(Block).all()
    blocks_list = [
        {"market_id": block.block_id, "market_name": block.block_name}
        for block in blocks
    ]
    db.close()

    # Збереження в JSON
    with open("data/markets.json", "w") as f:
        json.dump(blocks_list, f)
