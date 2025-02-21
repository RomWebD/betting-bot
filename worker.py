from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from database import SessionLocal
from betting_utils import get_name_of_blocks
from crud import add_blocks_to_db, add_markets_to_db


# Функція, яка буде виконуватись щодня
def update_blocks_daily():
    print("Запуск воркера для оновлення блоків...")

    # Підключення до БД
    db: Session = SessionLocal()
    try:
        # Отримання нових даних
        blocks, markets = get_name_of_blocks()

        # Оновлення в БД
        add_blocks_to_db(db, blocks)
        add_markets_to_db(db, markets)

        print("Дані успішно оновлено.")
    finally:
        db.close()


# Налаштування планувальника
def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_blocks_daily, "interval", days=1)
    scheduler.start()
    print("Планувальник запущено для щоденного оновлення даних.")
