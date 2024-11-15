import yaml
from sqlalchemy import create_engine
import pandas as pd

class DatabaseConnector:
    def __init__(self,creds_file = 'db_creds.yaml', local_file = 'local_creds.yaml'):
        self.creds_file = creds_file
        self.local_file = local_file
        self.engine = None
    #Reading credentials from db_creds.yaml file
    def read_db_creds(self):
        with open(self.creds_file, 'r') as f:
            data = yaml.safe_load(f)
        return data
    #Reading local credentials:
    def local_db_creds(self):
        with open(self.local_file, 'r') as f:
            data = yaml.safe_load(f)
        return data
    
    #Reads credentials using read_db_creds, constructs the PostgreSQL connection string, and creates a SQLAlchemy engine
    #Source engine
    def init_db_engine(self):
        data = self.read_db_creds()
        connection_string = f"postgresql://{data['RDS_USER']}:{data['RDS_PASSWORD']}@{data['RDS_HOST']}:{data['RDS_PORT']}/{data['RDS_DATABASE']}"
        self.engine = create_engine(connection_string)
        return self.engine
    
    #Local engine to connect sales_data db
    def init_db_engine1(self):
        data = self.local_db_creds()
        self.engine = create_engine(f"{data['DATABASE_TYPE']}+{data['DBAPI']}://{data['USER']}:{data['PASSWORD']}@{data['HOST']}:{data['PORT']}/{data['DATABASE']}")
        return self.engine

    
    def upload_to_db(self, df, tablename, engine=None):
        # Use the passed engine or the instance's engine
        if engine is None:
            engine = self.engine
            print(engine)

        if engine is None:
            raise ValueError("Engine is not initialized. Please check engine connection")

        # Upload the DataFrame to the specified table
        df.to_sql(tablename, con=engine, if_exists='replace', index=False)
        print(f"Data successfully '{tablename}' uploaded to the database")

    def upload_pdf_to_db(self, df, tablename, engine=None):
        # Use the passed engine or the instance's engine
        if engine is None:
            engine = self.engine
            print(engine)

        if engine is None:
            raise ValueError("Engine is not initialized. Please check engine connection")

        # Upload the DataFrame to the specified table
        df.to_sql(tablename, con=engine, if_exists='replace', index=False)
        print(f"Data successfully '{tablename}' uploaded to the database")

        




        
