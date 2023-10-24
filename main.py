import json
import logging
from general_cex import ExchangeHandler
from multiprocessing import Process


logging.basicConfig(
    filename="price_analyzer.log",
    filemode="a",
    format="[%(levelname)s] - %(asctime)s - %(name)s - %(processName)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger("Main")


def run(exchange):
    handler = ExchangeHandler(exchange)
    try:
        handler.update_price()
    except:
        logger.error(f"Error occurred during processing {exchange}", exc_info=True)


def main():
    with open("exchanges.json", "r") as exchanges_file:
        exchanges_info = json.load(exchanges_file)
    exchanges = exchanges_info.keys()
    for exchange in exchanges:
        Process(target=run, args=(exchange,), daemon=False, name=exchange).start()


if __name__ == "__main__":
    main()
