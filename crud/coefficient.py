from sqlalchemy.orm import Session
from models.coefficient import Coefficient


# Створення нового запису коефіцієнтів
def create_coefficient(
    db: Session,
    match_id: str,
    values: dict,
    score1: int,
    score2: int,
    cp: int,
    period: str,
    quarter_account,
    time: str,
):
    new_coefficient = Coefficient(
        match_id=match_id,
        values=values,
        score1=score1,
        score2=score2,
        period=period,
        quarter_account=quarter_account,
        time=time,
        cp=cp,
    )
    db.add(new_coefficient)
    db.commit()
    db.refresh(new_coefficient)
    return new_coefficient


# Отримання коефіцієнтів для матчу
def get_coefficients(db: Session, match_id: str):
    return db.query(Coefficient).filter(Coefficient.match_id == match_id).all()
