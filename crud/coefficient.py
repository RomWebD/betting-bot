from sqlalchemy.orm import Session
from models.coefficient import Coefficient


# Створення нового запису коефіцієнтів
def create_coefficient(
    db: Session, match_id: str, block_id: str, market_id: str, values: list
):
    coefficient = Coefficient(
        match_id=match_id, block_id=block_id, market_id=market_id, values=values
    )
    db.add(coefficient)
    db.commit()
    db.refresh(coefficient)
    return coefficient


# Отримання коефіцієнтів для матчу
def get_coefficients(db: Session, match_id: str):
    return db.query(Coefficient).filter(Coefficient.match_id == match_id).all()
