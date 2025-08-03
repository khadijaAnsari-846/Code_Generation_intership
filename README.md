📊 Financial Data Parser
--------------------------------------------------------------------------------


A modular Python-based CLI tool that automates the process of loading, cleaning, analyzing, and querying financial Excel files. 
It supports multi-file input, automatic column type detection, currency/date parsing, and stores cleaned data in SQLite for flexible querying.

🚀 Features
--------------------------------------------------------------------------------

✅ Load and preview multiple Excel files from a directory  
🔍 Detect column types automatically (date, number, string)  
🧼 Clean and parse:
   - Currency formats like $1,000, 1.2M, (500) to numeric  
   - Date formats including Q1-2024, 31-Dec-2023, Excel serials  
💾 Store cleaned data in SQLite database  
🔍 Query using filters and aggregation logic (SUM, AVG, etc.)  
🧱 Modular design (each phase isolated in separate module)  


🗂 Folder Structure
--------------------------------------------------------------------------------

financial-data-parser:
  - main.py  # Main entry point
  - data/  # Folder for raw Excel input files
  - cleaned_data/  # Stores cleaned Excel/SQLite DB output
  - src/
      core/:
        - main_design.py  # Menu loop & orchestrates all phases
        - phase_1.py  # Load and preview Excel files
        - phase_2.py  # Detect column types
        - phase_3.py  # Format amount and date columns
        - phase_4.py  # Store in SQLite and run queries
        - excel_processor.py  # ExcelProcessor class
        - type_detector.py  # Type detection logic
        - format_parser.py  # Cleans and converts financial/date data
        - data_storage.py  # SQLite DB wrapper for querying/aggregations
        - utils.py  # Common helpers (like file name fetcher)
        - __init__.py



🛠 Setup Instructions
--------------------------------------------------------------------------------

1. 📦 Install Required Packages

Run the following command to install all necessary libraries:

    pip install pandas openpyxl numpy

2. 📁 Add Input Files

Place your .xlsx files inside the data/ folder at the root of the project.

3. ▶ Run the Application

Execute the following command in your terminal from the project root:

    python main.py


💡 Additional Notes
--------------------------------------------------------------------------------

📁 You can add new .xlsx files anytime to data/, then re-run Phase 1 to process them.

🧠 Each class is reusable and loosely coupled (easy to scale and extend).

💾 The SQLite database is created inside cleaned_data/cleaned_data.db.
