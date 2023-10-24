import datetime
import logging

from sqlalchemy import DECIMAL
from sqlalchemy import Table, Column, Integer, String, MetaData, DateTime, Text
from sqlalchemy import create_engine, insert, text, bindparam, select

logging.basicConfig(
    filename="price_analyzer.log",
    filemode="a",
    format="[%(levelname)s] - %(asctime)s - %(name)s - %(processName)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger("Database")

with open(".env", "r") as file:
    keys = file.readlines()

connection_string = keys[0].split("=")[1].rstrip()


class DatabaseConnector(object):
    meta = MetaData()

    prices = Table(
        "prices", meta,
        Column('id', Integer, primary_key=True),
        Column('exchange', String(100)),
        Column('pair', Text),
        Column('bid', DECIMAL(26, 10)),
        Column('ask', DECIMAL(26, 10)),
        Column('timestamp', DateTime, default=datetime.datetime.now())
    )

    delta = Table(
        "delta", meta,
        Column("pair", Text),
        Column("exchange_1", String(100)),
        Column("exchange_2", String(100)),
        Column("delta", DECIMAL(10, 3)),
        Column("timestamp", DateTime, default=datetime.datetime.now())
    )

    historical_delta = Table(
        "historical_delta", meta,
        Column("pair", Text),
        Column("exchange_1", String(100)),
        Column("exchange_2", String(100)),
        Column("delta", DECIMAL(10, 3)),
        Column("timestamp", DateTime, default=datetime.datetime.now())
    )

    delta_cex = Table(
        "delta_cex", meta,
        Column("pair", Text),
        Column("exchange_1", String(100)),
        Column("exchange_2", String(100)),
        Column("delta", DECIMAL(10, 3)),
        Column("timestamp", DateTime, default=datetime.datetime.now())
    )

    def __init__(self, connection: str = connection_string):
        self.engine = create_engine(connection)
        self.meta.bind = self.engine
        self.meta.create_all()

    def price_insert_mass(self, exchange, data):
        conn = self.engine.connect()
        insert_query = insert(self.prices).values(exchange=exchange,
                                                  pair=bindparam("ticker"),
                                                  bid=bindparam("bid"),
                                                  ask=bindparam("ask"))
        conn.execute(insert_query, data)
        conn.close()
        self.engine.dispose()

    def select_pairs_cex(self):
        conn = self.engine.connect()
        query = text(
            """
            SELECT DISTINCT(pair) FROM prices WHERE exchange NOT LIKE "%@%";
            """
        )
        result = conn.execute(query).fetchall()
        pairs = [row[0] for row in result]
        conn.close()
        self.engine.dispose()
        return pairs

    def select_pairs_dex(self):
        conn = self.engine.connect()
        query = text(
            """
            SELECT DISTINCT(pair) FROM prices WHERE exchange LIKE "%@%";
            """
        )
        result = conn.execute(query).fetchall()
        pairs = [row[0] for row in result]
        conn.close()
        self.engine.dispose()
        return pairs

    def select_pairs_all(self):
        conn = self.engine.connect()
        query = text(
            """
            SELECT DISTINCT(pair) FROM prices;
            """
        )
        result = conn.execute(query).fetchall()
        pairs = [row[0] for row in result]
        conn.close()
        self.engine.dispose()
        return pairs

    def get_prices_by_pairs_cex(self, pair):
        conn = self.engine.connect()
        query = text(
            """
            SELECT exchange, bid, ask FROM prices WHERE pair = :pair 
            AND bid IS NOT NULL
            AND ask IS NOT NULL
            AND bid <> 0
            AND ask <> 0
            AND exchange NOT LIKE "%@%";
            """
        )
        result = conn.execute(query, pair=pair).fetchall()
        conn.close()
        self.engine.dispose()
        if len(result) != 0:
            return result

    def get_prices_by_pairs_dex(self, pair):
        conn = self.engine.connect()
        pairs_query = self.select_pairs_dex()
        pairs = tuple(set(i for i in pairs_query if i.startswith(pair)))
        query = text(
            """
            SELECT exchange, bid, ask FROM prices WHERE pair IN :pairs
            AND bid IS NOT NULL
            AND ask IS NOT NULL
            AND bid <> 0
            AND ask <> 0
            AND exchange LIKE "%@%";
            """
        )
        result = conn.execute(query, pairs=pairs).fetchall()
        conn.close()
        self.engine.dispose()
        if len(result) > 1:
            return result

    def get_prices_by_pairs_general(self, pair):
        conn = self.engine.connect()
        pairs_query = self.select_pairs_dex()
        pairs = [i for i in pairs_query if i.startswith(pair)]
        pairs.append(pair)
        pairs = tuple(pairs)
        query = text(
            """
            SELECT exchange, bid, ask FROM prices WHERE prices.pair IN :pairs
            AND bid IS NOT NULL
            AND ask IS NOT NULL
            AND bid <> 0
            AND ask <> 0;
            """
        )
        result = conn.execute(query, pairs=pairs, pair=pair).fetchall()
        conn.close()
        self.engine.dispose()
        if len(result) > 1:
            return result

    def insert_into_delta_cex(self, data):
        conn = self.engine.connect()
        insert_query = insert(self.delta_cex).values(pair=bindparam("ticker"),
                                                     exchange_1=bindparam("exchange_1"),
                                                     exchange_2=bindparam("exchange_2"),
                                                     delta=bindparam("delta"))
        conn.execute(insert_query, data)
        conn.close()
        self.engine.dispose()

    def insert_into_historical_delta(self, data):
        conn = self.engine.connect()
        insert_query = insert(self.historical_delta).values(pair=bindparam("ticker"),
                                                            exchange_1=bindparam("exchange_1"),
                                                            exchange_2=bindparam("exchange_2"),
                                                            delta=bindparam("delta"))
        conn.execute(insert_query, data)
        conn.close()
        self.engine.dispose()

    def select_delta_cex(self):
        conn = self.engine.connect()
        result = conn.execute(select(self.delta_cex)).fetchall()
        conn.close()
        self.engine.dispose()
        if result:
            return result
        else:
            return None

    def truncate_delta_cex(self):
        conn = self.engine.connect()
        conn.execute(text(
            """
            TRUNCATE delta_cex;
            """
        ))
        conn.close()
        self.engine.dispose()

    def truncate_prices(self):
        conn = self.engine.connect()
        conn.execute(text(
            """
            TRUNCATE prices;
            """
        ))
        conn.close()
        self.engine.dispose()
