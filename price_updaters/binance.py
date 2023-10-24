import json
from decimal import Decimal

import requests

from database_connector import DatabaseConnector

with open("../exchanges.json", "r") as exchanges_file:
    exchanges_info = json.load(exchanges_file)

with open("../usdt_pairs.json", "r") as pairs_file:
    pairs = json.load(pairs_file)
db = DatabaseConnector()


def price_updater(name_exchange):
    tickers_for_update = []
    url = exchanges_info[name_exchange]["price_endpoint"]
    formatted_pairs = [exchanges_info[name_exchange]["delimiter"].join(pair.split("_")) for pair in pairs]
    response = requests.get(url).json()
    for ticker in response:
        if ticker["symbol"] in formatted_pairs:
            if Decimal(ticker["bidPrice"]) * Decimal(ticker["bidQty"]) > Decimal("100") and \
                    Decimal(ticker["askPrice"]) * Decimal(ticker["askQty"]) > Decimal("100"):
                tickers_for_update.append({"b_pair": ticker["symbol"],
                                           "bid": Decimal(ticker["bidPrice"]),
                                           "ask": Decimal(ticker["askPrice"])})
    db.price_insert_mass(name_exchange, tickers_for_update)


if __name__ == "__main__":
    price_updater("Binance")
