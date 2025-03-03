import json
import requests
from cache import cache
import logging

from crud.matches import finish_match_by_id

# Логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_list_of_match():
    all_matches = []
    url = "https://betwinner.com/service-api/LiveFeed/Get1x2_VZip?sports=3&count=50&lng=en&gr=495&mode=4&country=27&partner=152&getEmpty=true&virtualSports=true&noFilterBlockEvent=true"
    req = requests.get(url)
    if req.status_code == 200:
        data = req.json()
        if data.get("Success") and data.get("Value"):
            values = data.get("Value")
            for value in values:
                try:
                    status = ""
                    match_id = value.get("I")
                    cps = value.get("SC", {}).get("CPS", "")
                    cp = value.get("SC", {}).get("CP", "")
                    # start_coef = value.get("E")
                    information = value.get("SC", {}).get("I", "")
                    # Визначення статусу:
                    if (
                        information == "The match has not started"
                        or information == "Pre-match betting"
                    ):
                        status = "scheduled"
                    # elif cps or start_coef:
                    elif cps:
                        status = "live"
                    elif not cps or cps == "Game finished":
                        status = "finished"

                    if cps != "Game finished":
                        current_data = [
                            {
                                "match_id": str(value.get("I")),  # ID
                                "league": value.get("LE"),  # league
                                "team1": value.get("O1E"),  # team1
                                "team2": value.get("O2E"),  # team2
                                "status": status,
                                "cps": value.get("SC").get("CPS"),  # CPS
                                "information": value.get("SC").get(
                                    "I"
                                ),  # additional information
                            }
                        ]
                        all_matches.extend(current_data)
                except Exception as err:
                    print(err)
    return all_matches


def extract_total_coefficients(data):
    coefficients = []

    # Проходимо всі коефіцієнти
    for coef in data:
        # Отримуємо назву блоку через cache
        block_name = (
            cache["blocks"].get(str(coef["GS"]), {}).get("block_name", "Unknown")
        )

        # Фільтруємо тільки ті, в яких є слово "Тотал"
        if "Total" in block_name:
            coefficients.append({"block_name": block_name, "coef": coef})

    return coefficients


# Функція для отримання коефіцієнтів
def fetch_coefficients(id):
    url = f"https://betwinner.com/service-api/LiveFeed/GetGameZip?id={id}&lng=en&isSubGames=true&GroupEvents=true&countevents=250&grMode=4&partner=152&topGroups=&country=27&marketType=1"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data
        # return data.get("Value", {}).get("GE", [])  # Отримуємо масив GE
    else:
        logger.error(f"Помилка запиту: {response.status_code}")
        return []


def seconds_to_minutes(time_in_seconds):
    minutes, seconds = divmod(int(time_in_seconds), 60)
    return f"{minutes:02d}:{seconds:02d}"


def filter_total_coefficients(coefficients, period_name=""):
    """Фільтрує коефіцієнти, де в block_name є слово 'Total'"""
    total_coefficients = []
    for coefs in coefficients:
        block_name = (
            cache["blocks"]
            .get(str(coefs.get("GS", "")), {})
            .get("block_name", "Unknown_Block")
        )
        if block_name == "Total":
            block_name = block_name + ". " + period_name if period_name else block_name
            coefficient_data = []

            for coef in coefs["E"]:
                for c in coef:
                    market_name = (
                        cache["markets"]
                        .get(str(c.get("T", "")), {})
                        .get("market_name", "Unknown_market")
                    )
                    market_name = (
                        market_name.replace("()", str(c["P"]))
                        if "()" in market_name
                        else market_name
                    )

                    coefficient_data.append({market_name: c.get("C")})

            total_coefficients.append(
                {"block_name": block_name, "coefficient_data": coefficient_data}
            )
            print()
        print()

    return total_coefficients


def extract_coefficients(data, key="GE"):
    """Витягує масив коефіцієнтів, якщо в об'єктах є ключ 'GE'"""
    extracted = []

    if key in data:
        extracted.extend(data[key])  # Додаємо в масив всі об'єкти з 'GE'

    return extracted


def get_coefficients_from_match(match_id=598606097):
    result = None
    try:
        total_additional_coefficients = []
        data = fetch_coefficients(match_id)
        if not data.get("Success") and not data.get("Value"):
            finish_match_by_id(match_id)
            return None

        informations = data.get("Value", {}).get("SC", [])
        time_in_seconds = informations.get("TS", "")
        # Яка чверть саме цифрою
        cp = informations.get("CP", "")
        if cp == 1 and not time_in_seconds:
            return None

        time_in_minute = seconds_to_minutes(time_in_seconds)

        # Який поточний рахунок
        curr_score = informations.get("FS")
        # Яка чверть текстом, наприклад - '4th quarter'
        curr_quarter = informations.get("CPS", "")
        # Рахунки по всіх зіграних чвертях
        quarter_account = informations.get("PS", "")
        quarter_account_obj = {item["Key"]: item["Value"] for item in quarter_account}

        coefficients = data.get("Value", {}).get("GE", {})
        if not coefficients:
            return None
        all_additional_coefficients = data.get("Value", {}).get("SG", [])
        for add_coefs in all_additional_coefficients:
            period_in_next = add_coefs.get("PN")
            if period_in_next and "quarter" in period_in_next:
                additional_coefficients = extract_coefficients(add_coefs)
                total_additional_coefficients.extend(
                    filter_total_coefficients(additional_coefficients, period_in_next)
                )
        total_coefficients = filter_total_coefficients(coefficients, curr_quarter)

        # Об'єднуємо результати, якщо потрібно
        all_total_coefficients = total_coefficients + total_additional_coefficients
        result = {
            "match_id": match_id,
            "time": time_in_minute,
            "cp": cp,
            "curr_quarter": curr_quarter,
            "curr_score": curr_score,
            "quarter_account": quarter_account_obj,
            "total_coefficients": all_total_coefficients,
        }

    except Exception as err:
        print(err)

    return result


def transform_data(data):
    blocks_list = []
    market_list = []
    unique_block_ids = set()  # Для зберігання унікальних block_id
    unique_market_ids = set()  # Для зберігання унікальних market_id

    for d in data:
        for c in data[d]:
            entity = data[d][c]
            blocks = entity["GN"]
            markets = entity["M"]
            # data_blocks = [
            #     {"block_id": key, "block_name": value} for key, value in blocks.items()
            # ]
            # data_market = [
            #     {"market_id": key, "market_name": value["N"]}
            #     for key, value in markets.items()
            # ]

            for key, value in blocks.items():
                if key not in unique_block_ids:
                    blocks_list.extend([{"block_id": key, "block_name": value}])
                    unique_block_ids.add(key)

            # Обробка маркетів з перевіркою на унікальність
            for key, value in markets.items():
                if key not in unique_market_ids:
                    market_list.extend([{"market_id": key, "market_name": value["N"]}])
                    unique_market_ids.add(key)
    return blocks_list, market_list


def get_name_of_blocks():
    blocks_list = None
    market_list = None
    url = "https://v3.traincdn.com/genfiles/cms/betstemplates/bets_model_short_en_all.json"
    req = requests.get(url)
    if req.status_code:
        result = json.loads(req.text)
    if result:
        blocks_list, market_list = transform_data(result)
    return blocks_list, market_list
