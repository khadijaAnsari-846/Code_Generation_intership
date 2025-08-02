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

def phase_3(processor, parser, detected_format):

    df_dict = processor.get_sheet_data() # Get the dictionary of sheet data

    if not df_dict:
        print("❌ No data available from Phase 1.")
        return None # Return None if no data


    # Assuming only one sheet was processed in Phase 1 and its data is in the dictionary
    # Get the first (and likely only) DataFrame from the dictionary
    sheet_name, df = list(df_dict.items())[0]


    # Cleaned copy of the DataFrame
    cleaned_df = df.copy()

    for col_name, info in detected_format.items():
        if col_name in cleaned_df.columns: # Check if column exists before processing
            if info['type'] == 'date':
                cleaned_df[col_name] = parser.parse_date(cleaned_df[col_name], info)
            elif info['type'] == 'number':
                 cleaned_df[col_name] = parser.parse_amount(cleaned_df[col_name], info)
            # else: # Keep other columns as they are (strings, unknown)
            #    pass
        else:
             print(f"⚠️ Warning: Column '{col_name}' from detected format not found in DataFrame.")


    print("\n✅ Cleaned Data Preview:")
    print(cleaned_df.head())

    # Optionally: offer to save
    save = input("Do you want to save cleaned data to Excel? (y/n): ")
    if save.lower() == 'y':
        # Construct a valid filename, replacing potential invalid characters
        safe_sheet_name = re.sub(r'[^\w\s.-]', '_', sheet_name)
        current_dir = os.path.dirname(__file__)
        root_dir = os.path.abspath(os.path.join(current_dir, "..", ".."))
        data_dir = os.path.join(root_dir, "clean_data")
        
        output_filename = data_dir+"/"+f"{safe_sheet_name}_cleaned.xlsx"
        try:
            cleaned_df.to_excel(output_filename, index=False)
            print(f"📁 Saved as '{output_filename}'")
        except Exception as e:
            print(f"❌ Error saving file: {e}")


    return cleaned_df # Return the cleaned DataFrame




