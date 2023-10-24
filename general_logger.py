import logging
import os
import datetime


if os.path.exists(f"logs/{datetime.datetime.now().strftime('%Y')}/{datetime.datetime.now().strftime('%m')}"):
    pass
else:
    os.makedirs(f"logs/{datetime.datetime.now().strftime('%Y')}/{datetime.datetime.now().strftime('%m')}")

filename = f"logs/{datetime.datetime.now().strftime('%Y')}/{datetime.datetime.now().strftime('%m')}/" \
            f"triangle_arbitrage.log"

logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] - %(asctime)s - %(name)s - %(message)s',
                    filename="price_comparator.log",
                    filemode="a")


def get_logger(name):
    return logging.getLogger(name)
