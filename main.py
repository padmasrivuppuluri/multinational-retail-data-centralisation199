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

    # List all tables in the source database 
    tables = data_extractor.list_db_tables()
    print("Tables in the source database:", tables)

    # Extract data from a specific table ('legacy_users')
    data = data_extractor.read_rds_table('legacy_users')  
    data = pd.DataFrame(data) 
    #print(type(data)) 

    # Initialize the DataCleaning class and clean the extracted data (for CSV data)
    '''
    data_cleaning = DataCleaning(data)
    cleaned_csv = data_cleaning.clean_user_data()
    print(cleaned_csv)
    data_extractor.convert_df_csv(cleaned_csv,csv_file='cleaned_users_data.csv')

    # Upload the cleaned data to the local database in the 'dim_users' table
    tablename = 'dim_users'
    db_connector.upload_to_db(cleaned_csv, tablename, engine=local_engine)  

    # Retrieve the PDF data using Tabula 
    pdf_link = 'https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf'
    pdf_data = data_extractor.retrieve_pdf_data(pdf_link)
    print(type(pdf_data))
        
    # Clean PDF data
    pdf_cleaning = DataCleaning(data=pdf_data)  
    cleaned_pdf = pdf_cleaning.clean_card_data()
    print(cleaned_pdf)
    
    # Upload cleaned PDF data to the local database
    pdf_tablename = 'dim_card_details'
    db_connector.upload_to_db(cleaned_pdf, pdf_tablename, engine=local_engine)
'''
    # Define headers and URLs
    headers = {'x-api-key': 'yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX'}
    number_stores_url = "https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/number_stores"
    store_details_base_url = "https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details"

    # Instantiate and use the DataExtractor class
    data_extractor = DataExtractor(headers=headers)
    num_stores = data_extractor.get_number_of_stores(number_stores_url)
    print(num_stores)

    stores_df = data_extractor.get_store_data(store_details_base_url, num_stores)
    print(stores_df)

   #Clean store data
    store_data_cleaning = DataCleaning(data=stores_df)
    cleaned_store_data =store_data_cleaning.called_clean_store_data()
    print(cleaned_store_data)
    store_data_cleaning.cleaned_store_csv('cleaned_store_file.csv')

    store_tablename = 'dim_store_details'
    db_connector.upload_to_db(cleaned_store_data,store_tablename,engine=local_engine)
'''
    #extract product dettails data using aws s3
    data = data_extractor.extract_from_s3(s3_address="s3://data-handling-public/products.csv")
    print(data)
    csv_file = data_extractor.convert_df_csv(data, csv_file= "products.csv")

    
    data_cleaning = DataCleaning(data)
    clean_products_data =data_cleaning.clean_products_data()
    print(clean_products_data)
    data_extractor.convert_df_csv(clean_products_data,csv_file='cleaned_products.csv')

    products_tablename = 'dim_products'
    db_connector.upload_to_db(clean_products_data,products_tablename,engine=local_engine)

      
    #Extracting data from orders table
    
    data = data_extractor.read_rds_table('orders_table')
    data = pd.DataFrame(data) 
    print(data) 

    csv_file = data_extractor.convert_df_csv(data, csv_file= "orders_data.csv")
    data_cleaning = DataCleaning(data)
    clean_orders_data = data_cleaning.clean_orders_data()
    print(clean_orders_data)
    data_cleaning.cleaned_csv('cleaned_orders.csv')

    #Upload orders data to db
    orders_table_name = 'orders_table'
    db_connector.upload_to_db(clean_orders_data,orders_table_name,engine=local_engine)

    data = data_extractor.extract_eventsdata_from_s3(s3_address="https://data-handling-public.s3.eu-west-1.amazonaws.com/date_details.json")
    print(data)
    print(type(data))
    data_cleaning=DataCleaning(data)
    cleaned_events_data = data_cleaning.clean_date_events_data()
    print(cleaned_events_data)

    date_events_tablesname = 'dim_date_times'
    db_connector.upload_to_db(cleaned_events_data,date_events_tablesname,engine=local_engine)

'''

    




    




    
     