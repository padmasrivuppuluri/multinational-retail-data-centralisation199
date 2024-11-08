import yaml
from sqlalchemy import create_engine
class DatabaseConnector:
    def __init__(self,creds_file = 'db_creds.yaml'):
        self.creds_file = creds_file

    #Reading credentials from db_creds.yaml file
    def read_db_creds(self):
        with open(self.creds_file, 'r') as f:
            data = yaml.safe_load(f)
        return data
    
    #Reads credentials using read_db_creds, constructs the PostgreSQL connection string, and creates a SQLAlchemy engine
    def init_db_engine(self):
        data = self.read_db_creds()
        connection_string = f"postgresql://{data['RDS_USER']}:{data['RDS_PASSWORD']}@{data['RDS_HOST']}:{data['RDS_PORT']}/{data['RDS_DATABASE']}"
        engine = create_engine(connection_string)
        return engine
    
db_connector = DatabaseConnector()
credentials = db_connector.init_db_engine()
print(credentials)

        
