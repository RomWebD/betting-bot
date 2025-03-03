from apscheduler.schedulers.background import BackgroundScheduler
from worker import update_blocks_daily
from workers.coefficient_worker import store_coefficients
from workers.match_worker import update_matches_in_live, update_scheduled_and_live_matches


# Налаштування планувальника
def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_blocks_daily, "interval", days=1)
    scheduler.add_job(store_coefficients, "interval", seconds=20)
    scheduler.add_job(update_matches_in_live, "interval", minutes=1)
    # scheduler.add_job(update_scheduled_and_live_matches, 'cron', hour=17, minute=5)

    scheduler.start()
    print("Планувальник запущено для щоденного оновлення даних.")
