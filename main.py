from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import Base, engine
from routes import router
from worker import start_scheduler
from cache import cache_all_tables


# Lifespan для FastAPI
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Події startup
    print("Запуск Lifespan: startup")
    Base.metadata.create_all(bind=engine)  # Створення таблиць
    start_scheduler()  # Запуск планувальника
    # Якщо JSON-файл не існує, створюємо його
    cache_all_tables()

    yield  # Очікує завершення роботи сервера

    # Події shutdown
    print("Завершення Lifespan: shutdown")


# Ініціалізація FastAPI з Lifespan
app = FastAPI(lifespan=lifespan)

# Підключаємо маршрути
app.include_router(router)
