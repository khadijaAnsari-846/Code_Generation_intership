import pandas as pd
import os
from IPython.display import display
import sqlite3
import re
import warnings
from collections import Counter
warnings.filterwarnings("ignore", category=UserWarning)  # Suppress the warning



class DataStorage:
    def __init__(self, db_path=":memory:"):
        self.conn = sqlite3.connect(db_path)  # default is in-memory DB
        self.cursor = self.conn.cursor()
        self.loaded_tables = set()

    def store_data(self, dataframe: pd.DataFrame, table_name: str):
        # Save DataFrame to SQLite table
        dataframe.to_sql(table_name, self.conn, if_exists='replace', index=False)
        self.loaded_tables.add(table_name)
        print(f"✅ Table '{table_name}' stored in SQLite database.")

    def query_by_sql(self, sql: str) -> pd.DataFrame:
        try:
            return pd.read_sql_query(sql, self.conn)
        except Exception as e:
            print(f"❌ SQL Error: {e}")
            return pd.DataFrame()

    def close(self):
        self.conn.close()
        print("🔒 SQLite connection closed.")
