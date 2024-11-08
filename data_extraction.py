from sqlalchemy import inspect
import pandas as pd
import tabula

class DataExtractor:
    def __init__(self,engine):
        self.engine = engine
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

    #To retrieve pdf data
    def retrieve_pdf_data(self,pdf_link):
        df  = tabula.read_pdf(pdf_link, pages='all')
        return df
    
    
    
  
    

