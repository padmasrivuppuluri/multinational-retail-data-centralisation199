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
        
    #Cleaning card_details data in pdf file
    def clean_card_data(self):
        print(f"The rows before removing NULL values: {self.df.shape[0]}")
        self.df.replace('NULL', pd.NA, inplace= True)
        self.df.dropna(inplace= True)
        print(f"The number of rows after removing null values: {self.df.shape[0]}")
        if 'card_number' in self.df.columns:
            self.df.drop_duplicates(subset='card_number',inplace=True)
            self.df['card_number'] = self.df['card_number'].astype(str)

        # Remove entries with any non-numeric characters
            self.df['card_number'] = self.df['card_number'].apply(lambda x: re.sub(r'[^\d]', '', x))

            # Filter out empty strings or invalid card numbers that became empty after removal of characters
            self.df = self.df[self.df['card_number'].str.isdigit()]

            # Convert valid entries to numeric type
            self.df.loc[:, 'card_number'] = pd.to_numeric(self.df['card_number'])
            print(f"The rows after converting 'card_number' to numeric values,: {self.df.shape[0]}")
            self.df = self.df.dropna(subset=['card_number'])
            print(f"The rows after removing invalid 'card_numbers': {self.df.shape[0]}")
        if 'expiry_date' in self.df.columns:
            self.df['expiry_date'] = pd.to_datetime(self.df['expiry_date'],format='%m/%y', errors='coerce')
        self.df.dropna(subset = 'expiry_date',inplace= True)
                    
        if 'date_payment_confirmed' in self.df.columns:
            self.df.loc[:, 'date_payment_confirmed'] = pd.to_datetime(self.df['date_payment_confirmed'], errors='coerce')
        return self.df
    
    #Cleaning store_details_data
    def called_clean_store_data(self):
        self.df.replace('NULL', pd.NA, inplace=True)
        #self.df.dropna(inplace = True)
        print(f"No. of rows {self.df.shape}")
        
       #Convert "opening_date" column into a datetime data type
        if 'opening_date' in self.df.columns:
            self.df['opening_date'] = pd.to_datetime(self.df['opening_date'],format= 'mixed',errors='coerce')
        self.df.dropna(subset = ['opening_date'],inplace= True)

        self.df['staff_numbers'] = self.df['staff_numbers'].str.replace(r'[^0-9]', '', regex=True)
        return self.df
    
    def cleaned_store_csv(self,clean_file = 'cleaned_store_file.csv'):
        self.df.to_csv(clean_file, index=False)

    def convert_weight(self, value):
        try:
            value = value.lower().replace(' ', '')  # Ensure consistent formatting
            if 'kg' in value:
                return float(value.replace('kg', '').strip())  # Convert to float and assume kg
            elif 'g' in value:
                # Handle cases like '16x10g' or '8x150g'
                match = re.match(r'(\d+)[xX](\d+)g', value)
                if match:
                    quantity, grams = match.groups()
                    return int(quantity) * int(grams) / 1000  # Convert total grams to kg
                else:
                    return float(value.replace('g', '').strip()) / 1000  # Convert grams to kg
            elif 'ml' in value:
                # Assume density of 1g/ml (i.e., 1 ml = 1 g), convert to kg
                return float(value.replace('ml', '').strip()) / 1000
            else:
                return None  # Ignore other units like ml or invalid values
        except (ValueError, AttributeError):
            return None  # Handle non-convertible values

    def convert_product_weights(self):
        if 'weight' in self.df.columns:
            self.df['weight'] = self.df['weight'].apply(self.convert_weight)
            self.df.dropna(subset=['weight'], inplace=True)
            self.df['weight'] = self.df['weight'].apply(lambda x: f"{x:.5f}kg")
        else:
            print("Warning: 'weight' column not found in the DataFrame.")
        return self.df 
     
    # Cleaning products data
    def clean_products_data(self):
        self.df.replace('NULL', pd.NA, inplace=True)
        self.df.dropna(inplace=True)
        self.convert_product_weights()
        return self.df
    
    #Cleaning orders data
    def clean_orders_data(self):
        columns_to_remove = ['first_name','last_name','1']
        self.df.drop(columns=[col for col in columns_to_remove if col in self.df.columns], inplace=True)
        return self.df
    
    #Cleaning date_events_data
    def clean_date_events_data(self):
        self.df.replace('NULL', pd.NA, inplace=True)
        self.df.dropna(inplace=True)

        for column in ['day', 'month','year']:
            if column in self.df.columns:
                self.df[column] =pd.to_numeric(self.df[column],errors= 'coerce')
            self.df.dropna(inplace=True)
            return self.df
       


        


