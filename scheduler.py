from apscheduler.schedulers.background import BackgroundScheduler
from worker import update_blocks_daily


# Налаштування планувальника
def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_blocks_daily, "interval", days=1)
    scheduler.start()
    print("Планувальник запущено для щоденного оновлення даних.")
