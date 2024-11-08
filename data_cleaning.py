import pandas as pd
import numpy as np

class DataCleaning:
    def __init__(self, data=None, pdf_data=None):
        if data is not None:
            self.df = pd.DataFrame(data)
        elif pdf_data is not None:
            if isinstance(pdf_data, (list, dict)):
              self.df = pd.DataFrame(pdf_data)
        else:
            raise ValueError("Either 'data' or 'pdf_data' must be provided.")
    #Cleaning data in csv file
    def clean_user_data(self):
        if self.df is None:
            raise ValueError("No data provided for cleaning CSV data.")
        
        # Step 1: Replace "NULL" strings with NaN
        self.df.replace('NULL', np.nan, inplace=True)
        self.df.dropna(inplace=True)

        if 'join_date' in self.df.columns:
            self.df['join_date'] = pd.to_datetime(self.df['join_date'], errors='coerce')
        return self.df
    
    def cleaned_csv(self,clean_file = 'cleaned_file.csv'):
        self.df.to_csv(clean_file, index=False)
    
    #Cleaning data in pdf file
    def clean_card_data(self):
        if self.df is not None:
            # Corrected reference to 'self.df' instead of 'self.df1'
            self.df.replace('NULL', np.nan, inplace=True)
            self.df.dropna(inplace=True)

            if 'card_number' in self.df.columns:
                self.df.drop_duplicates(subset='card_number', inplace=True)
                self.df['card_number'] = pd.to_numeric(self.df['card_number'], errors='coerce')
                self.df.dropna(subset=['card_number'], inplace=True)

            if 'date_payment_confirmed' in self.df.columns:
                self.df['date_payment_confirmed'] = pd.to_datetime(self.df['date_payment_confirmed'], errors='coerce')

            return self.df
        else:
            raise ValueError("No data to clean for PDF.")
    

        



