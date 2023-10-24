import csv
import os
import json

from pairs_by_exchange import gate_pairs_parser, binance_pairs_parser

functions_list = dir()


def parsing_pairs():
    gate_pairs_parser()
    binance_pairs_parser()


def compare_pairs():
    file_list = os.listdir("trading_pairs")
    all_pairs = []
    for filename in file_list:
        with open(f"trading_pairs/{filename}") as json_file:
            exchange_pairs = json.load(json_file)
        all_pairs.extend(exchange_pairs)
    unique_pairs = list(set(all_pairs))
    unique_pairs.sort()
    with open("unique_pairs.json", "w") as unique_file:
        json.dump(unique_pairs, unique_file)


def pairs_report_to_json():
    file_list = os.listdir("trading_pairs")
    all_trading_pairs = {}
    for filename in file_list:
        exchange_name = filename.split("_")[0].capitalize()
        with open(f"trading_pairs/{filename}") as pairs_file:
            tickers = json.load(pairs_file)
        all_trading_pairs[exchange_name] = {
            "pairs": tickers,
            "pairs_quantity": len(tickers)
        }
    with open("all_trading_pairs.json", "w") as summary_file:
        json.dump(all_trading_pairs, summary_file)


def pairs_report_to_csv():
    file_list = os.listdir("trading_pairs")
    with open("summary_exchanges.csv", "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(("Exchange", "Pairs qty"))

    for filename in file_list:
        exchange_name = filename.split("_")[0].capitalize()
        with open(f"trading_pairs/{filename}") as pairs_file:
            tickers = json.load(pairs_file)

        with open("summary_exchanges.csv", "a", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow((exchange_name, len(tickers)))


def usdt_pair_searcher():
    with open("unique_pairs.json") as unique_files:
        unique_pairs = json.load(unique_files)
    usdt_pairs = []
    for pair in unique_pairs:
        if pair.startswith("USDT") or pair.endswith("USDT"):
            usdt_pairs.append(pair)
    with open("usdt_pairs.json", "w") as usdt_pair_file:
        json.dump(usdt_pairs, usdt_pair_file)


parsing_pairs()
compare_pairs()
usdt_pair_searcher()
