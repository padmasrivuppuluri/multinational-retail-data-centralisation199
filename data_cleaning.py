import pandas as pd
import numpy as np
import re

class DataCleaning:
    def __init__(self, data=None):
        if data is not None:
            if isinstance(data, pd.DataFrame):
                self.df = data
        else:
            raise ValueError("The 'data' parameter must be provided.")
        
    #Cleaning data in csv file
    def clean_user_data(self):
        if self.df is None:
            raise ValueError("No data provided for cleaning CSV data.")
        
        # Step 1: Replace "NULL" strings with NaN
        self.df.replace('NULL', pd.NA, inplace=True)
        self.df.dropna(inplace= True)
        print(f"The number of rows after removing Nan values: {self.df.shape[0]}")

        if 'date_of_birth' in self.df.columns:
            self.df['date_of_birth'] = pd.to_datetime(self.df['date_of_birth'],format= 'mixed',errors='coerce')
        self.df.dropna(subset = 'date_of_birth',inplace= True)

        if 'join_date' in self.df.columns:
            self.df['join_date'] = pd.to_datetime(self.df['join_date'], errors='coerce')
        return self.df
    
    def cleaned_csv(self,clean_file = 'cleaned_file.csv'):
        self.df.to_csv(clean_file, index=False)
        
    
    #Cleaning data in pdf file
    def clean_card_data(self):
        print(f"The rows before removing NULL values: {self.df.shape[0]}")
        self.df.replace('NULL', pd.NA, inplace= True)
        self.df.dropna(inplace= True)
        print(f"The number of rows after removing null values: {self.df.shape[0]}")
        if 'card_number' in self.df.columns:
            self.df.drop_duplicates(subset='card_number',inplace=True)
            print(f"The rows after removing duplicate card numbers: {self.df.shape[0]}")
            self.df['card_number'] = self.df['card_number'].astype(str)
            self.df = self.df[self.df['card_number'].str.isdigit()]
            self.df['card_number'] = pd.to_numeric(self.df['card_number'])
            print(f"The rows after converting 'card_number' to numeric values,: {self.df.shape[0]}")
            # Step 5: Remove rows where 'card_number' is NaN after coercion
            self.df.dropna(subset=['card_number'], inplace=True)
            print(f"The rows after removing 'card_number' to NaN values,:{self.df.shape[0]}")
        if 'date_payment_confirmed' in self.df.columns:
            self.df['date_payment_confirmed'] = pd.to_datetime(self.df['date_payment_confirmed'], errors='coerce')
        return self.df
    
    def called_clean_store_data(self):
        # Replace multiple variations of 'NULL' with NaN in all columns
        self.df.replace('NULL', np.nan, inplace=True)
       # self.df.dropna(inplace = True)
        print(f"No. of rows {self.df.shape}")

        #Convert "opening_date" column into a datetime data type
        self.df['opening_date'] = pd.to_datetime(self.df['opening_date'], errors='coerce', dayfirst=True)

        # Drop rows with NaT (invalid dates) in 'opening_date'
        self.df.dropna(subset=['opening_date'], inplace=True)

        self.df['staff_numbers'] = self.df['staff_numbers'].str.replace(r'[^0-9]', '', regex=True)
        return self.df
    
    def cleaned_store_csv(self,clean_file = 'cleaned_store_file.csv'):
        self.df.to_csv(clean_file, index=False)

    def convert_weight(self, value):
        if pd.isna(value):
            return None
        value = str(value).lower().strip()
        value = re.sub(r'[^0-9\.a-z]', '', value)

        if 'kg' in value:
                return float(value.replace('kg', '').strip())
        elif 'g' in value:
            try:
                return float(value.replace('g', '').strip()) / 1000
            except ValueError:
                return None
        elif 'ml' in value:
            try:
                return float(value.replace('ml', '').strip()) / 1000
            except ValueError:
                return None
        else:
            try:
                return float(value)
            except ValueError:
                return None

    def convert_product_weights(self):
        if 'weight' in self.df.columns:
            self.df['weight'] = self.df['weight'].apply(self.convert_weight)
            self.df.dropna(subset=['weight'], inplace=True)
        else:
            print("Warning: 'weight' column not found in the DataFrame.")
        return self.df
    
    def clean_products_data(self):
        self.df.replace('NULL', np.nan, inplace=True)
        self.df.dropna(inplace=True)
        self.convert_product_weights()
        return self.df
    
    def clean_orders_data(self):
        columns_to_remove = ['first_name','last_name','1']
        self.df.drop(columns=[col for col in columns_to_remove if col in self.df.columns], inplace=True)
        return self.df
    def clean_date_events_data(self):
        self.df.replace('NULL', np.nan, inplace=True)
        self.df.dropna(inplace=True)

        for column in ['day', 'month','year']:
            if column in self.df.columns:
                self.df[column] =pd.to_numeric(self.df[column],errors= 'coerce')
            self.df.dropna(inplace=True)
            return self.df
       


        


