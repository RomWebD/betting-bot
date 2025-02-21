import json
from pathlib import Path
from database import SessionLocal
from models import Block, Market

# Загальні налаштування
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

# Словник для кешування різних моделей
CACHE_CONFIG = {
    "blocks": {
        "model": Block,
        "json_file": DATA_DIR / "blocks.json",
        "id_field": "block_id",
        "fields": ["block_id", "block_name"],
    },
    "markets": {
        "model": Market,
        "json_file": DATA_DIR / "markets.json",
        "id_field": "market_id",
        "fields": ["market_id", "market_name"],
    },
}

# Глобальні змінні для кешу
cache = {"blocks": {}, "markets": {}}


# Функція для вивантаження даних в JSON (словник зі швидким доступом)
def load_to_json(model, json_file, id_field, fields):
    db = SessionLocal()
    data = db.query(model).all()
    # Створюємо словник зі швидким доступом за ключем ID
    data_dict = {
        str(getattr(item, id_field)): {field: getattr(item, field) for field in fields}
        for item in data
    }
    db.close()

    # Зберігаємо як словник в JSON
    with open(json_file, "w") as f:
        json.dump(data_dict, f)

    return data_dict  # Повертаємо словник для глобальної змінної


# Функція для отримання даних з JSON
def get_from_json(json_file):
    if json_file.exists():
        with open(json_file, "r") as f:
            return json.load(f)
    return {}


# Функція для кешування всіх таблиць
def cache_all_tables():
    for key, config in CACHE_CONFIG.items():
        json_file = config["json_file"]
        id_field = config["id_field"]

        # Якщо JSON існує – завантажуємо, якщо ні – створюємо
        if json_file.exists():
            cache[key] = get_from_json(json_file)
        else:
            cache[key] = load_to_json(
                config["model"], json_file, id_field, config["fields"]
            )
