import numpy as np
import pandas as pd
import os
from IPython.display import display
import openpyxl
from openpyxl import load_workbook,Workbook
import re
from datetime import datetime
from decimal import Decimal
import locale
import re
import warnings
from collections import Counter
warnings.filterwarnings("ignore", category=UserWarning)  # Suppress the warning
from datetime import datetime, timedelta

def phase_2(processor,typeDetector):
    #1.
  print("\n############### Phase 2 #######################\n")
  print("************************* Analyze Columns *******************")
  

  sheet_data = processor.get_sheet_data()


  if sheet_data:
    # Access the single item in the dictionary
    sheet_name, df = list(sheet_data.items())[0]

    store_type_detect=typeDetector.analyze_column(df)

    print("\n\n Here is Type Detected dictionary::")
    print(store_type_detect)
    return store_type_detect

  else:
    print("No sheet Found!!")

