import json
from sqlalchemy.orm import Session
from models.market import Market
from database import SessionLocal


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


def load_markets_from_db():
    db = SessionLocal()
    markets = db.query(Market).all()
    blocks_list = [
        {"market_id": market.market_id, "market_name": market.market_name}
        for market in markets
    ]
    db.close()

    # Збереження в JSON
    with open("data/markets.json", "w") as f:
        json.dump(blocks_list, f)
