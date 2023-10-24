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
        if ticker.upper() in formatted_pairs:
            try:
                if (Decimal(response[ticker]["bids"][0][0]) * Decimal(response[ticker]["bids"][0][1]) > Decimal(
                        "100") and Decimal(response[ticker]["asks"][0][0]) *
                        Decimal(response[ticker]["asks"][0][1]) > Decimal("100")):
                    tickers_for_update.append({"b_pair": "".join(ticker
                                                                 .split(exchanges_info[name_exchange]["delimiter"])),
                                               "bid": Decimal(response[ticker]["bids"][0][0]),
                                               "ask": Decimal(response[ticker]["asks"][0][0])})
            except KeyError:
                continue
    db.price_insert_mass(name_exchange, tickers_for_update)


if __name__ == "__main__":
    price_updater("Gate")
