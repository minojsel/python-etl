import os
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine, text
from .loader import Loader
from ..utils.logger import logger

load_dotenv()

class PostgreSQLLoader(Loader):
    def __init__(self):
        self._username = os.getenv('PSQL_USER')
        self._password = os.getenv('PSQL_PASS')
        self._host     = os.getenv('PSQL_HOST')
        self._port     = os.getenv('PSQL_PORT')
        self._db       = os.getenv('PSQL_DB')
        self._schema   = os.getenv('PSQL_SCHEMA', None)
        self._conn     = self.get_connection()
    
    @logger
    def get_connection(self):
        if self._schema:
            return create_engine(f'postgresql://{self._username}:{self._password}@{self._host}:{self._port}/{self._db}', connect_args={'options': f'-csearch_path={self._schema}'})
        else:
            return create_engine(f'postgresql://{self._username}:{self._password}@{self._host}:{self._port}/{self._db}')
    
    @logger
    def load(self, data: pd.DataFrame, table: str, if_exists='append'):
        """
        Load the Pandas dataframe into PostgreSQL database
        """
        data.to_sql(table, self._conn, if_exists=if_exists, index=False)

    @logger
    def execute(self, query):
        """
        Execute custom queries against the database.
        """
        with self._conn.connect() as conn:
            conn.execute(text(query))
            conn.commit()