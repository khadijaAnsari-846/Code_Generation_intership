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




class FormatParser:
    def __init__(self):
        self.__value = None
        self.__format = None

    def normalize_currency(self, value: str) -> str:
        value = value.strip()

        # Remove unwanted symbols but keep digits, comma, dot, parentheses, minus
        value = re.sub(r"[^\d.,()\-\s]", "", value)

        # Handle (1,234.56) → -1234.56
        if value.startswith("(") and value.endswith(")"):
            value = "-" + value[1:-1]

        # Handle 1234.56- → -1234.56
        if value.endswith("-"):
            value = "-" + value[:-1]

        # Handle European format: 1.234,56 → 1234.56
        if "." in value and "," in value and value.rfind(",") > value.rfind("."):
            value = value.replace(".", "").replace(",", ".")
        else:
            value = value.replace(",", "")  # US/Indian: remove commas

        return value

    def handle_special_format(self, value: str) -> str:
        value = value.upper().strip()

        multiplier = 1
        if value.endswith("K"):
            multiplier = 1_000
            value = value[:-1]
        elif value.endswith("M"):
            multiplier = 1_000_000
            value = value[:-1]
        elif value.endswith("B"):
            multiplier = 1_000_000_000
            value = value[:-1]

        try:
            numeric_value = float(value)
            return str(numeric_value * multiplier)
        except Exception:
            return value  # return original if can't parse

    def parse_amount(self, column: pd.Series, format_info: dict) -> pd.Series:
        cleaned_col = []

        for val in column:
            try:
                if pd.isnull(val):
                    cleaned_col.append(None)
                    continue

                val = str(val)
                val = self.handle_special_format(val)
                val = self.normalize_currency(val)
                cleaned_col.append(float(val))
            except Exception:
                cleaned_col.append(None)

        return pd.Series(cleaned_col, name=column.name)

    def parse_date(self, column: pd.Series, format_info: dict) -> pd.Series:
        parsed_dates = []

        for val in column:
            try:
                if pd.isnull(val):
                    parsed_dates.append(None)
                    continue

                # ✅ Already datetime
                if isinstance(val, (datetime, pd.Timestamp)):
                    parsed_dates.append(val.date())
                    continue

                # ✅ Excel serial number
                if isinstance(val, int) or (str(val).isdigit() and len(str(val)) >= 5):
                    base = datetime(1899, 12, 30)
                    parsed = base + timedelta(days=int(val))
                    parsed_dates.append(parsed.date())
                    continue

                # ✅ String-based parsing
                val = str(val).strip()

                for fmt in [
                    "%m/%d/%Y", "%d/%m/%Y", "%Y-%m-%d",
                    "%d-%b-%Y", "%d-%B-%Y", "%b %Y", "%B %Y"
                ]:
                    try:
                        parsed = datetime.strptime(val, fmt)
                        parsed_dates.append(parsed.date())
                        break
                    except:
                        continue
                else:
                    # ✅ Quarter format: Q1 2024
                    if "Q" in val.upper():
                        q_match = re.search(r"[Qq](\d)[\s\-]?(?:\d{2,4})", val)
                        y_match = re.search(r"(?:20)?(\d{2,4})", val)
                        if q_match and y_match:
                            quarter = int(q_match.group(1))
                            year = int(y_match.group(1))
                            if year < 100:
                                year += 2000
                            month = (quarter - 1) * 3 + 1
                            parsed = datetime(year, month, 1)
                            parsed_dates.append(parsed.date())
                            continue

                    parsed_dates.append(None)

            except Exception:
                parsed_dates.append(None)

        return pd.Series(parsed_dates, name=column.name)
