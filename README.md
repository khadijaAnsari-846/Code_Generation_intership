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
See in flow_of_dictories.txt



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
