import json
import requests


def get_data_from_match(id=598606097):
    all_coefficients = []
    url = f"https://betwinner.com/service-api/LiveFeed/GetGameZip?id={id}&isSubGames=true&GroupEvents=true&countevents=250&grMode=4&partner=152&topGroups=&country=31&marketType=1"
    req = requests.get(url)
    result = json.loads(req.text)
    if result.get("Success") and result.get("Value"):
        values = result.get("Value")
        print(values)
    print(result)


def transform_data(data):
    blocks_list = []
    market_list = []
    for d in data:
        for c in data[d]:
            entity = data[d][c]
            blocks = entity["GN"]
            markets = entity["M"]
            data_blocks = [
                {"block_id": key, "block_name": value} for key, value in blocks.items()
            ]
            data_market = [
                {"market_id": key, "market_name": value["N"]}
                for key, value in markets.items()
            ]
            blocks_list.extend(data_blocks)
            market_list.extend(data_market)
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
