import json
import re

import requests

with open("exchanges.json", "r") as exchanges_info_file:
    exchanges_info = json.load(exchanges_info_file)


def binance_pairs_parser():
    trading_pairs = []
    base_url = exchanges_info["Binance"]["pairs_endpoint"]
    response = requests.get(url=base_url).json()["symbols"]
    for ticker in response:
        if ticker["status"] != "BREAK" and ticker["isSpotTradingAllowed"] is not False:
            if not re.search(r'\d[SLsl]', ticker["symbol"]) and "$" not in ticker["symbol"]:
                pair = f"{ticker['baseAsset'].upper()}_{ticker['quoteAsset'].upper()}"
                trading_pairs.append(pair)
    with open("trading_pairs/binance_pairs.json", "w") as pairs_file:
        json.dump(trading_pairs, pairs_file)


def gate_pairs_parser():
    trading_pairs = []
    base_url = exchanges_info["Gate"]["pairs_endpoint"]
    response = requests.get(url=base_url).json()
    for ticker in response:
        if ticker["trade_status"] == "tradable":
            if not re.search(r'\d[SLsl]', ticker["id"]) and "$" not in ticker["id"]:
                trading_pairs.append(ticker["id"].upper())
    with open("trading_pairs/gate_pairs.json", "w") as pairs_file:
        json.dump(trading_pairs, pairs_file)
