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




class DataTypeDetector:
    def __init__(self):
        self.__dataTypeStore = {}
        self.__null_counts = {}

        # Common date formats for business data
        self.common_date_formats = [
            "%Y-%m-%d", "%d-%m-%Y", "%m/%d/%Y",
            "%Y%m%d", "%d.%m.%Y", "%Y/%m/%d",
            "%m-%d-%Y", "%d/%m/%Y"
        ]

    def detect_date_format(self, sample_values, threshold=0.7):
        if len(sample_values) == 0:
            return False

        sample_values = sample_values.astype(str)

        # First try common business date formats
        for date_format in self.common_date_formats:
            try:
                parsed = pd.to_datetime(sample_values, format=date_format, errors='coerce')
                success_rate = parsed.notna().mean()
                if success_rate >= threshold:
                    return True
            except:
                continue

        # Fallback to flexible parsing if no format matches
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                parsed = pd.to_datetime(sample_values, errors='coerce')
                success_rate = parsed.notna().mean()
                return success_rate >= threshold
        except:
            return False

    def detect_number_format(self, sample_values, threshold=0.7):
        if len(sample_values) == 0:
            return False

        def clean_number(val):
            if pd.isna(val):
                return val
            val = str(val).strip()
            # Handle European-style numbers (1.000,00)
            if ',' in val and '.' in val:
                val = val.replace('.', '').replace(',', '.')
            # Remove non-numeric chars except digits, ., -
            val = re.sub(r'[^\d\.-]', '', val)
            return val

        cleaned = sample_values.apply(clean_number)
        try:
            parsed = pd.to_numeric(cleaned, errors='coerce')
            success_rate = parsed.notna().mean()
            return success_rate >= threshold
        except:
            return False

    def classify_string_type(self, column_name, sample_values):
        col = column_name.lower()

        # Check for common patterns in column names
        if any(key in col for key in ['name', 'account', 'customer']):
            return "name"
        elif any(key in col for key in ['desc', 'note', 'narration', 'message']):
            return "description"
        elif any(key in col for key in ['type', 'group', 'category', 'subtype']):
            return "category"
        elif any(key in col for key in ['code', 'id']):
            return "identifier"
        elif any(key in col for key in ['address', 'location', 'city']):
            return "address"
        else:
            # Check content for common patterns
            str_values = sample_values.astype(str)
            if str_values.str.match(r'^[A-Z]{3}$').mean() > 0.8:  # Currency codes
                return "currency"
            elif str_values.str.match(r'^[A-Z]{2}\d+$').mean() > 0.5:  # Product codes
                return "product_code"
            return "generic"

    def analyze_column(self, data):
        print("Check Null Values Per Column:\n")
        null_counts = data.isnull().sum()
        print(null_counts)
        self.__null_counts = null_counts.to_dict()
        print("************************* Detect Type of columns *******************\n")
        print("\nDetecting column types...\n")

        for col in data.columns:
            self.__dataTypeStore[col] = {
                'type': None,
                'subtype': None,
                'null_count': null_counts[col]
            }

            # Get non-null samples (minimum 5, maximum 20)
            sample_size = min(20, max(5, len(data[col].dropna())))
            sample_values = data[col].dropna().head(sample_size)

            if len(sample_values) == 0:
                print(f"⚠️ Column '{col}' is empty - marking as unknown")
                self.__dataTypeStore[col]['type'] = "unknown"
                continue

            # Check for date first
            if self.detect_date_format(sample_values):
                print(f"🗓️ Column '{col}' detected as: date")
                self.__dataTypeStore[col]['type'] = "date"
                continue

            # Then check for numbers
            if self.detect_number_format(sample_values):
                print(f"🔢 Column '{col}' detected as: number")
                self.__dataTypeStore[col]['type'] = "number"

                # Additional numeric subtype detection
                values = pd.to_numeric(data[col].dropna(), errors='coerce')
                if (values % 1 == 0).all():
                    self.__dataTypeStore[col]['subtype'] = "integer"
                else:
                    self.__dataTypeStore[col]['subtype'] = "float"
                continue

            # Finally classify strings
            string_type = self.classify_string_type(col, sample_values)
            print(f"🔤 Column '{col}' detected as: string ({string_type})")
            self.__dataTypeStore[col]['type'] = "string"
            self.__dataTypeStore[col]['subtype'] = string_type

        return self.__dataTypeStore