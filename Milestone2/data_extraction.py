from sqlalchemy import inspect
import pandas as pd
import tabula
import requests
import json
import boto3

class DataExtractor:
    def __init__(self,engine=None,headers = None):
        self.engine = engine
        self.headers = headers
    #list_db_tables takes the engine as a parameter, uses SQLAlchemy’s inspect to retrieve the list of table names, and returns them.
    def list_db_tables(self):
        inspector = inspect(self.engine)
        tables = inspector.get_table_names()
        return tables
    
    #Method to read a specific table and return it as a pandas DataFrame
    def read_rds_table(self,tablename):
        df = pd.read_sql_table(tablename, con = self.engine)
        return df
    
    def convert_df_csv(self, df, csv_file="data.csv"):
        df.to_csv(csv_file, index=False)
        return csv_file
    
    #To retrieve pdf data
    def retrieve_pdf_data(self,pdf_link):
        df  = tabula.read_pdf(pdf_link, pages='all')
        combined_df = pd.concat(df)
        return combined_df
    #API
    def get_number_of_stores(self, url):
        """Retrieve and return the number of stores from the API."""
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
           data = response.json()
           number_stores = data.get('number_stores')
           return number_stores
        else:
          print(f"Request failed with status code: {response.status_code}")
          print(f"Response Text: {response.text}")
          return None
    def get_store_data(self, base_url, number_of_stores):
        """Retrieve store data for all stores and return it as a DataFrame."""
        store_data = []
        for store_number in range(0, number_of_stores + 1):
            url = f"{base_url}/{store_number}"
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                store_data.append(response.json())
            elif response.status_code == 500:
                print(f"Error fetching data for store {store_number}: 500 (server error). Skipping this store.")
            # Handle any other errors (e.g., 404, 400) by logging them
            else:
                print(f"Error fetching data for store {store_number}: {response.status_code}")        
        # Return the store data as a DataFrame
        return pd.DataFrame(store_data)
    
    def convert_json_to_csv(self, json_data, csv_file="output.csv"):
        df = pd.DataFrame(json_data)
        # Save DataFrame as a CSV file
        df.to_csv(csv_file, index=False)
        return csv_file
    
    #Extracting product details data from AWS s3
    def extract_from_s3(self, s3_address):
        #url = s3://data-handling-public/products.csv 
        bucket_name = "data-handling-public"
        key = "products.csv"
        local_filename = "C:/Users/new user/Downloads/products.csv"
        s3 = boto3.client('s3')
        s3.download_file(bucket_name, key, local_filename)
        df = pd.read_csv(local_filename)
        return df
    #extracting  date events data drom AWS s3
    def extract_eventsdata_from_s3(self,s3_address):
        bucket_name = "data-handling-public"
        key = "date_details.json"
        local_filename = "C:/Users/new user/Downloads/date_details.json"
        s3 = boto3.client('s3')
        s3.download_file(bucket_name, key, local_filename)
        df = pd.read_json(local_filename)
        return df






    
    
  
    

