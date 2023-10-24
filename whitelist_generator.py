import json

import requests

with open("exchanges.json", "r") as exchanges_info_file:
    exchanges_info = json.load(exchanges_info_file)


def binance_pairs_parser():
    trading_pairs = []
    base_url = exchanges_info["Binance"]["pairs_endpoint"]
    response = requests.get(url=base_url).json()["symbols"]
    for ticker in response:
        if ticker['baseAsset'] == "USDT" or ticker['quoteAsset'] == "USDT":
            if ticker['status'] == 'TRADING':
                trading_pairs.append(f"{ticker['baseAsset']}_{ticker['quoteAsset']}")
    return trading_pairs


def gate_pairs_parser():
    trading_pairs = []
    base_url = exchanges_info["Gate"]["pairs_endpoint"]
    response = requests.get(url=base_url).json()
    for ticker in response:
        if ticker['base'] == "USDT" or ticker['quote'] == "USDT":
            if ticker['trade_status'] == 'tradable':
                trading_pairs.append(f"{ticker['base']}_{ticker['quote']}")
    return trading_pairs


def generator():
    binance_pairs = binance_pairs_parser()
    gate_pairs = gate_pairs_parser()
    result_pairs = [pair for pair in binance_pairs if pair in gate_pairs]
    with open("whitelist.json", "w") as white_file:
        json.dump(result_pairs, white_file)


generator()
