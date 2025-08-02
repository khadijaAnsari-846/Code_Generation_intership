import numpy as np
import pandas as pd
import os
from IPython.display import display
import openpyxl
from openpyxl import load_workbook,Workbook
import sqlite3
import re
from datetime import datetime
from decimal import Decimal
import locale
import re
import warnings
from collections import Counter
warnings.filterwarnings("ignore", category=UserWarning)  # Suppress the warning
from datetime import datetime, timedelta
from src.core.data_storage import DataStorage


def phase_4(dataStorage,clear_df):
  

    # ✅ Load cleaned Excel data
    df = clear_df.copy()

   

    # Get the absolute project root
    current_dir = os.path.dirname(__file__)
    project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))

    # Construct the clean_data folder path
    clean_data_folder = os.path.join(project_root, "clean_data")
    os.makedirs(clean_data_folder, exist_ok=True)  # ✅ Ensure it exists

    # Define full path to database
    db_path = os.path.join(clean_data_folder, "cleaned_data.db")

    # Create DataStorage instance with the path
    # ✅ Initialize SQLite storage
    db = DataStorage(db_path)
    db.store_data(df, table_name="Clean Data Sheet")

    print("\n📌 Running Queries on SQLite-stored Data:\n")

    # 🔍 1. Get all invoices above 10,000
    sql1 = """
        SELECT *
        FROM ledger
        WHERE "Document Type" = 'Invoice' AND "Amount (LCY)" > 10000
    """
    result1 = db.query_by_sql(sql1)
    print("🔍 Invoices > 10,000:\n", result1.head(), "\n")

    # 📊 2. Total amount per Customer
    sql2 = """
        SELECT "Customer Name", SUM("Amount (LCY)") AS TotalAmount
        FROM ledger
        GROUP BY "Customer Name"
        ORDER BY TotalAmount DESC
        LIMIT 10
    """
    result2 = db.query_by_sql(sql2)
    print("📊 Top 10 Customers by Total Amount:\n", result2, "\n")

    # 📅 3. Count documents per Posting Date
    sql3 = """
        SELECT "Posting Date", COUNT(*) AS DocumentCount
        FROM ledger
        GROUP BY "Posting Date"
        ORDER BY "Posting Date" ASC
    """
    result3 = db.query_by_sql(sql3)
    print("📅 Document Count per Posting Date:\n", result3.head(), "\n")

    # 🏷️ 4. Document types frequency
    sql4 = """
        SELECT "Document Type", COUNT(*) AS Count
        FROM ledger
        GROUP BY "Document Type"
    """
    result4 = db.query_by_sql(sql4)
    print("🏷️ Document Type Distribution:\n", result4, "\n")

    # 💰 5. Average Remaining Amount per Customer
    sql5 = """
        SELECT "Customer Name", AVG("Remaining Amount") AS AvgRemaining
        FROM ledger
        GROUP BY "Customer Name"
        ORDER BY AvgRemaining DESC
        LIMIT 10
    """
    result5 = db.query_by_sql(sql5)
    print("💰 Top 10 Customers by Avg Remaining Amount:\n", result5, "\n")

    # 🔍 6. Get documents where remaining amount is exactly zero
    sql6 = """
        SELECT *
        FROM ledger
        WHERE "Remaining Amount" = 0
        LIMIT 5
    """
    result6 = db.query_by_sql(sql6)
    print("✅ Fully Paid Documents (Remaining Amount = 0):\n", result6, "\n")

    # 📦 7. All customers having more than 5 entries
    sql7 = """
        SELECT "Customer Name", COUNT(*) AS EntryCount
        FROM ledger
        GROUP BY "Customer Name"
        HAVING COUNT(*) > 5
        ORDER BY EntryCount DESC
    """
    result7 = db.query_by_sql(sql7)
    print("📦 Customers with More Than 5 Entries:\n", result7, "\n")

    # ✅ Close the DB connection
    db.close()



