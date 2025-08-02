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
from src.core.utils import get_file_name

def phase_1(processor):
  file_paths=get_file_name()

  #1.
  print("\n############### Phase 1 #######################\n")
  print("************************* Load File *******************")

  processor.load_files(file_paths)

  #2.
  print("\n***********************Get sheet info*****************")
  sheet_names =processor.get_sheet_info()

  #3.
  print("\n***********************Extract data*********************")
  sheet_list = [sheet for sheets in sheet_names.values() for sheet in sheets]
  print(f"Available sheets: {sheet_list}")
  id = input(f"Enter an index of the sheet whose data you want to see (0-{len(sheet_list)-1}): ")

  while not id.isdigit() or int(id) >= len(sheet_list):
      id = input(f"Enter a valid index within the sheet range (0-{len(sheet_list)-1}): ")

  selected_sheet_index = int(id)
  selected_sheet_name = sheet_list[selected_sheet_index]

  
  for workbook_path, sheets_in_workbook in sheet_names.items():
    if selected_sheet_name in sheets_in_workbook:
      print(f"Extracting data for sheet '{selected_sheet_name}' from workbook '{workbook_path}'")
      processor.extract_data(workbook_path, selected_sheet_name) # Pass both workbook path and sheet name
      break # Assuming sheet names are unique across workbooks, stop after finding it

  #4.
  print("\n***********************Preview data*********************")
  processor.preview_data(rows=5)






