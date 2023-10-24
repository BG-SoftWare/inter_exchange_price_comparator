from database_connector import DatabaseConnector

db = DatabaseConnector()


if __name__ == "__main__":
    db.truncate_prices()