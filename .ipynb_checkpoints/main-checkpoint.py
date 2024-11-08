from database_utils import DatabaseConnector
from data_extraction import DataExtractor

if __name__ == "__main__":
    # Initialize the DatabaseConnector and create an engine
    db_connector = DatabaseConnector()
    engine = db_connector.init_db_engine()

    # Initialize the DataExtractor with the engine
    data_extractor = DataExtractor(engine)

    # List all tables in the database
    tables = data_extractor.list_db_tables()
    print("Tables in the database:", tables)

    data = data_extractor.read_rds_table('legacy_users')
    print(data)