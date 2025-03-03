from crud.matches import add_or_update_matches, get_finished_matches
from betting_utils import get_list_of_match


# Функція, яка буде виконуватись кожні 5 хвилин
def update_matches_in_live():
    print("Запуск воркера для МАТЧІВ у лайві...")

    try:
        # Отримання нових даних
        matches = get_list_of_match()

        # Оновлення в БД

        add_or_update_matches(matches)
    except Exception as err:
        print(err)


def update_scheduled_and_live_matches():
    get_finished_matches()
