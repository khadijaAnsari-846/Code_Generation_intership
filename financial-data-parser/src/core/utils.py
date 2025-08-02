import numpy as np
import pandas as pd
import os



import os

import os

import os

def get_file_name():
    import os

    current_dir = os.path.dirname(__file__)
    root_dir = os.path.abspath(os.path.join(current_dir, "..", ".."))
    data_dir = os.path.join(root_dir, "data")

    if not os.path.exists(data_dir):
        raise FileNotFoundError(f"❌ Folder not found: {data_dir}")

    file_paths = [
        os.path.join(data_dir, filename)
        for filename in os.listdir(data_dir)
        if filename.lower().endswith(".xlsx")  # handles both `.xlsx` and `.XLSX`
    ]

    return file_paths



