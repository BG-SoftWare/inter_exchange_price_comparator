from decimal import Decimal

import requests

from database_connector import DatabaseConnector
from general_logger import get_logger

logger = get_logger("Price Comparator")
db = DatabaseConnector()


def price_handler_cex():
    logger.info("Start price comparing")
    old_delta_cex = db.select_delta_cex()
    db.truncate_delta_cex()

    if old_delta_cex is not None:
        old_tickers_list = list(set([row[0] for row in old_delta_cex]))
    else:
        old_tickers_list = []
    pairs = db.select_pairs_cex()
    result = []

    for pair in pairs:
        info = price_analyze_cex(pair)
        if len(info) > 0:
            result.extend(info)
    if len(result) > 0:
        sorted_data = sorted(result, key=lambda x: x["delta"], reverse=True)
        try:
            db.insert_into_delta_cex(sorted_data)
            db.insert_into_historical_delta(sorted_data)
            logger.info("Insert into delta CEX and Historical Delta. Status: SUCCESS")
        except Exception as e:
            logger.error("Insert into delta CEX and Historical Delta. Status: FAILED", e)
        new_delta_info = {}

        for new_delta in result:
            if new_delta["ticker"] not in old_tickers_list:
                if new_delta["ticker"] not in new_delta_info.keys():
                    new_delta_info[new_delta['ticker']] = {"min_delta": new_delta["delta"],
                                                           "max_delta": new_delta["delta"]}
                else:
                    if new_delta["delta"] >= new_delta_info[new_delta['ticker']]["max_delta"]:
                        new_delta_info[new_delta['ticker']]["max_delta"] = new_delta["delta"]
                    elif new_delta["delta"] <= new_delta_info[new_delta['ticker']]["min_delta"]:
                        new_delta_info[new_delta['ticker']]["min_delta"] = new_delta["delta"]

        if len(new_delta_info) > 0:
            message = ""
            for element in new_delta_info:
                message += f"For {element} min delta is: " \
                           f"{new_delta_info[element]['min_delta']} %, " \
                           f"max delta is: {new_delta_info[element]['max_delta']} %\n"
            message_report_to_telegram(message)


def price_analyze_cex(pair):
    info_for_report = []
    try:
        prices = db.get_prices_by_pairs_cex(pair)
        for index, price in enumerate(prices):
            for index_1, price_1 in enumerate(prices):
                if index == index_1:
                    continue
                if price[1] > price_1[2]:
                    delta = (Decimal(price[1]) - Decimal(price_1[2])) / Decimal(price_1[2]) * Decimal("100")
                    # 20 and 20000 are the boundary values between which the script will react
                    if Decimal("20") < delta < Decimal("20000"):
                        info_for_report.append({"ticker": pair,
                                                "exchange_1": price[0],
                                                "exchange_2": price_1[0],
                                                "delta": delta.quantize(Decimal("0.01"))})
        return info_for_report
    except Exception:
        return []


def message_report_to_telegram(message):
    with open("/root/price_screener/.env", "r") as file:
        keys = file.readlines()
    api_token = keys[1].split("=")[1].rstrip()
    chat_id = keys[3].split("=")[1].rstrip()
    url = f"https://api.telegram.org/bot{api_token}"
    method = url + "/sendMessage"
    response = requests.post(method, data={
        "chat_id": int(chat_id),
        "text": message,
        "protect_content": True
    })
    if response.status_code != 200:
        logger.warning("Message has not been sent")


if __name__ == "__main__":
    try:
        logger.info("Start handler")
        price_handler_cex()
        logger.info("handler has finished work. Status: SUCCESS")
    except:
        logger.critical("handler hasn't finished work. Status: FAIL", exc_info=True)
