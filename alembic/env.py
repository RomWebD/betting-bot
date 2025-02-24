from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context


# Імпорт налаштувань
from config import settings

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config


# Імпорт моделей
from models import Base

# Налаштування MetaData для моделей
target_metadata = Base.metadata

# Налаштування URL для підключення до БД
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,  # Враховувати зміни типів полів
        )

        with context.begin_transaction():
            context.run_migrations()


run_migrations_online()
