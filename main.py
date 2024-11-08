from database_utils import DatabaseConnector
from data_extraction import DataExtractor
from data_cleaning import DataCleaning
import pandas as pd

if __name__ == "__main__":
    # Initialize the DatabaseConnector and create the source engine (for RDS)
    db_connector = DatabaseConnector()
    source_engine = db_connector.init_db_engine()  # Connect to the source DB (e.g., RDS)
    print("Source Engine:", source_engine)

    # Initialize the local engine (for sales_data database)
    local_engine = db_connector.init_db_engine1()  
    print("Local Engine:", local_engine)
    
    # Initialize the DataExtractor with the source engine (RDS)
    data_extractor = DataExtractor(source_engine)

    # List all tables in the source database (e.g., RDS)
    tables = data_extractor.list_db_tables()
    print("Tables in the source database:", tables)

    # Extract data from a specific table ('legacy_users')
    data = data_extractor.read_rds_table('legacy_users')  
    data = pd.DataFrame(data) 
    print(type(data)) 
    

    # Initialize the DataCleaning class and clean the extracted data (for CSV data)
    csv_cleaning = DataCleaning(data)  
    cleaned_csv = csv_cleaning.clean_user_data()
    print(cleaned_csv)
    csv_cleaning.cleaned_csv('cleaned_file.csv')

    # Upload the cleaned data to the local database in the 'dim_users' table
    tablename = 'dim_users'
    db_connector.upload_to_db(cleaned_csv, tablename, engine=local_engine)  

    # Retrieve the PDF data using Tabula 
    pdf_link = 'https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf'
    pdf_data = data_extractor.retrieve_pdf_data(pdf_link)
    print(type(pdf_data))
    
    pdf_data_df = pd.DataFrame([pdf_data])
    print(type(pdf_data_df))
        
    # Clean PDF data
    pdf_cleaning = DataCleaning(data=pdf_data_df)  
    cleaned_pdf = pdf_cleaning.clean_card_data()

    
    