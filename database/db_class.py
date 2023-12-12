import logging
from sqlalchemy import create_engine
import configparser
import os
import sys

# Get the absolute path to the current script/executable
app_path = os.path.abspath(os.path.dirname(sys.argv[0]))

# Construct the path to the .ini file
config_path = os.path.join(app_path, 'database', 'db_config.ini')

with open(config_path, 'r', encoding='utf-8') as f:
    config_content = f.read()

config = configparser.ConfigParser()
config.read_string(config_content)

# Get a logger
logger = logging.getLogger(__name__)


class Database:
    def __init__(self, db_config):
        """
        Initialize the Database object.

        Parameters:
        - db_config: Configuration dictionary containing the database parameters
        """
        self.connection = None
        self.sql_server = db_config['sql_server']['server']
        self.sql_database = db_config['sql_server']['database']
        self.sql_username = db_config['sql_server']['username']
        self.sql_password = db_config['sql_server']['password']

    def connect(self):
        """
        Establish a connection to the database.

        Returns:
        - Connection object: If successful.
        - None: Otherwise.
        """
        return self.connect_sql_server()

    def connect_sql_server(self):
        """
        Establish a connection to a SQL Server database.

        Returns:
        - Connection object: If successful.
        - None: Otherwise.
        """

        try:
            connection_string = (f"mssql+pyodbc://{self.sql_username}:{self.sql_password}@"
                                 f"{self.sql_server}/{self.sql_database}?driver=ODBC+Driver+17+for+SQL+Server")
            self.connection = create_engine(connection_string)
            return self.connection
        except Exception as e:
            logger.error(f"An error occurred while connecting to the SQL Server database: {e}")
            return None
