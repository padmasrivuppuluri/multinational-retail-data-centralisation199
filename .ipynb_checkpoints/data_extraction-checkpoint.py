from sqlalchemy import inspect
import pandas as pd

class DataExtractor:
    def __init__(self,engine):
        self.engine = engine
    #list_db_tables takes the engine as a parameter, uses SQLAlchemy’s inspect to retrieve the list of table names, and returns them.
    def list_db_tables(self):
        inspector = inspect(self.engine)
        tables = inspector.get_table_names()
        return tables
    
    #Method to read a specific table and return it as a pandas DataFrame
    def read_rds_table(self,tablename, output_filename="data.csv"):
        df = pd.read_sql_table(tablename, con = self.engine)
        df.to_csv(output_filename, index=False)
        print(f"Data from {tablename} has been saved to {output_filename}")
        return df
    
  
    

