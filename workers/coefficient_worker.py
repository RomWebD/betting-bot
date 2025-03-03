from sqlalchemy.orm import Session
from betting_utils import get_coefficients_from_match
from crud.matches import get_live_matches
from database import SessionLocal
from crud.coefficient import create_coefficient
import logging

# Логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Функція для обробки та запису коефіцієнтів
def store_coefficients():
    logger.info("Оновлення коефіцієнтів...")
    db: Session = SessionLocal()
    # Отримання коефіцієнтів для всіх live-матчів
    live_matches = get_live_matches()
    for match in live_matches:
        match_id = match.match_id
        coefficients = get_coefficients_from_match(match_id)
        if coefficients:
            match_id = coefficients.get("match_id")
            values = coefficients.get("total_coefficients")
            score1 = str(
                coefficients.get("curr_score", {}).get("S1", 0),
            )
            score2 = str(
                coefficients.get("curr_score", {}).get("S2", 0),
            )
            period = coefficients.get("curr_quarter", "")
            cp = coefficients.get("cp", "")
            quarter_account = coefficients.get("quarter_account", [])
            time = coefficients.get("time", "")

            print()
            create_coefficient(
                db=db,
                match_id=match_id,
                values=values,
                score1=score1,
                score2=score2,
                cp=cp,
                period=period,
                quarter_account=quarter_account,
                time=time,
            )

    db.close()
    logger.info("Коефіцієнти оновлено.")
