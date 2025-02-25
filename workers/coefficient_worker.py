from sqlalchemy.orm import Session
from betting_utils import get_coefficients_from_match
from database import SessionLocal
from crud.coefficient import create_coefficient
from cache import cache
import logging

# Логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Функція для обробки та запису коефіцієнтів
def store_coefficients():
    logger.info("Оновлення коефіцієнтів...")
    db: Session = SessionLocal()

    coefficients = get_coefficients_from_match()

    for coeff in coefficients:
        match_id = coeff.get("match_id")
        block_id = coeff.get("block_id")
        market_id = coeff.get("market_id")
        values = coeff.get("values")
        score1 = coeff.get("score1", 0)
        score2 = coeff.get("score2", 0)
        period = coeff.get("period", "")
        cps = coeff.get("cps", "")
        add_info = coeff.get("add_info", "")
        time = coeff.get("time", "")

        # Перевіряємо чи існують Block та Market
        if block_id in cache["blocks"] and market_id in cache["markets"]:
            create_coefficient(
                db, match_id, block_id, market_id, values, score1, score2, period, time
            )

    db.close()
    logger.info("Коефіцієнти оновлено.")
