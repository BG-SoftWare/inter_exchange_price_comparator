import json
import logging
from concurrent.futures import ThreadPoolExecutor
from decimal import Decimal

import requests

from database_connector import DatabaseConnector

logging.basicConfig(
    filename="price_analyzer.log",
    filemode="a",
    format="[%(levelname)s] - %(asctime)s - %(name)s - %(processName)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger("Exchange Handler")


class ExchangeHandler:
    def __init__(self, name_exchange: str):
        self.name_exchange = name_exchange
        self.exchanges_info = {}
        self.pairs = []
        self._file_reader()
        self.db = DatabaseConnector()

    def _file_reader(self):
        with open("exchanges.json", "r") as exchanges_file:
            self.exchanges_info = json.load(exchanges_file)

        with open("whitelist.json", "r") as pairs_file:
            self.pairs = json.load(pairs_file)

    def __mass_price_update(self, url: str):
        logger.info(f"{self.name_exchange}")
        tickers_for_update = []
        exchanges_routes = self.exchanges_info[self.name_exchange]
        blacklist = exchanges_routes['blacklist']
        formatted_pairs = [exchanges_routes["delimiter"].join(pair.split("_")).upper()
                           for pair in self.pairs if pair not in blacklist]
        response = requests.get(url).json()
        match self.name_exchange:
            case "Gate":
                for ticker in response:
                    if ticker.upper() in formatted_pairs:
                        try:
                            tickers_for_update.append({
                                "ticker": "".join(ticker.split(exchanges_routes["delimiter"])).upper(),
                                "bid": Decimal(response[ticker]["bids"][0][0]),
                                "ask": Decimal(response[ticker]["asks"][0][0])})
                        except KeyError:
                            logger.warning(f"Empty depth {ticker.upper()}")
                            continue
                        except Exception:
                            logger.warning(f"Some error occurred during processing {ticker.upper()}", exc_info=True)

            case _:
                if isinstance(response, dict) and "data" in response.keys():
                    try:
                        response = response["data"]["ticker"]
                    except:
                        response = response["data"]
                elif isinstance(response, dict) and "result" in response.keys():
                    try:
                        response = response["result"]["list"]
                    except:
                        try:
                            response = response["result"]["data"]
                        except:
                            response = response["result"]
                elif isinstance(response, dict) and "ticker" in response.keys():
                    response = response["ticker"]
                for ticker in response:
                    if ticker[exchanges_routes["symbol"]].upper() in formatted_pairs:
                        try:
                            pair = "".join(ticker[exchanges_routes["symbol"]].
                                           split(exchanges_routes["delimiter"])).upper()
                        except ValueError:
                            pair = ticker[exchanges_routes["symbol"]].upper()
                        try:
                            tickers_for_update.append({"ticker": pair,
                                                       "bid": Decimal(ticker[exchanges_routes["bid_price"]]),
                                                       "ask": Decimal(ticker[exchanges_routes["ask_price"]])})
                        except KeyError:
                            continue
        self.db.price_insert_mass(self.name_exchange, tickers_for_update)

    def __price_update_by_pair_name(self, url: str):
        logger.info(f"{self.name_exchange}")
        pair_urls = []
        blacklist = self.exchanges_info[self.name_exchange]["blacklist"]
        for pair in self.pairs:
            if pair not in blacklist:
                if self.exchanges_info[self.name_exchange]["case"] == "upper":
                    pair_for_replace = self.exchanges_info[self.name_exchange]["delimiter"] \
                        .join(pair.split("_")).upper()
                else:
                    pair_for_replace = self.exchanges_info[self.name_exchange]["delimiter"] \
                        .join(pair.split("_")).lower()
                pair_url = url.replace("{pair_name}", pair_for_replace)
                pair_urls.append((pair_url, "".join(pair.split("_"))))
        if self.name_exchange:
            max_workers = 2
        else:
            max_workers = 12
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            result = []
            for url in pair_urls:
                try:
                    prices = executor.submit(self.__get_price, url[0]).result()
                    if prices is not None:
                        prices["ticker"] = url[1]
                        result.append(prices)
                except:
                    logger.info("Probably this pair absent on this exchange", exc_info=True)
        self.db.price_insert_mass(self.name_exchange, result)

    def __get_price(self, pair_url: str) -> dict | None:
        response = requests.get(pair_url)
        if response.status_code == 200:
            response = response.json()
        else:
            return None
        if "message" in response.keys():
            logger.warning(response)
            return None
        if "data" in response:
            response = response["data"]
            if response["bids"] is None and response["asks"] is None:
                logger.warning(f"On exchange {self.name_exchange} and pair {pair_url} absent info about depth")
                logger.warning(response)
        try:
            return {"bid": Decimal(response["bids"][0][0]),
                    "ask": Decimal(response["asks"][0][0])}
        except Exception:
            logger.warning("Some error", exc_info=True)
            return None

    def update_price(self):
        logger.info(f"Start processing exchange {self.name_exchange}")
        url = self.exchanges_info[self.name_exchange]["price_endpoint"]
        if "{pair_name}" in url:
            self.__price_update_by_pair_name(url)
        else:
            self.__mass_price_update(url)
