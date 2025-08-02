from src.core.excel_processor import ExcelProcessor
from src.core.format_parser import FormatParser
from src.core.data_storage import DataStorage
from src.core.type_detector import DataTypeDetector
from src.core.phase_1 import phase_1
from src.core.phase_2 import phase_2
from src.core.phase_3 import phase_3
from src.core.phase_4 import phase_4
import pandas as pd
import numpy as np


def main():
    # Phase status tracking
    processor = ExcelProcessor()
    typeDetector = DataTypeDetector()
    formatParser = FormatParser() # Keep parser instance
    dataStorage = DataStorage() # Initialize DataStorage here

    phase1_done = False
    phase2_done = False
    phase3_done = False
    phase4_done = False
    store_type_data={}
    cleaned_data_available = False # Track if cleaned data is ready for storage
    cleaned_df = pd.DataFrame() # Initialize cleaned_df outside the loop


    while True:

        print("\n\n========== MAIN MENU ==========\n")
        print(":::Just for Guidance: (Some phases are dependent on each other, so order matters):::")
        print("1. ▶ Phase 1: Load and Preview Excel Files")
        print("2. ▶ Phase 2: Detect Column Types")
        print("3. ▶ Phase 3: Parse Amounts and Dates")
        print("4. ▶ Phase 4: Store and Query Data")
        print("0. Exit")

        choice = input("\nChoose Carefully! Select an option: ")

        if choice == '1':
            phase_1(processor)
            phase1_done = True
            print("\n✅ PHASE 1 COMPLETED SUCCESSFULLY")

        elif choice == '2':
            if not phase1_done:
                print("❌ Phase 1 must be completed before Phase 2.")
            else:
                store_type_data = phase_2(processor, typeDetector)
                if store_type_data: # Check if type detection was successful
                    phase2_done = True
                    print("\n✅ PHASE 2 COMPLETED SUCCESSFULLY")
                else:
                     print("\n❌ PHASE 2 FAILED")


        elif choice == '3':
            if not phase2_done:
                print("❌ Phase 2 must be completed before Phase 3.")
            else:
                # Phase 3 cleans the data and makes it available for storage
                cleaned_df = phase_3(processor,formatParser,store_type_data) # Capture the returned DataFrame
                if cleaned_df is not None:
                     cleaned_data_available = True # Data is now cleaned and ready
                     phase3_done = True # Mark phase 3 as done
                     print("🚧 Phase 3: COMPLETED SUCCESSFULLY")
                else:
                     
                     print("\n❌ PHASE 3 FAILED - No data cleaned.")


        elif choice == '4':
            if not phase3_done or not cleaned_data_available:
                print("❌ Phase 3 must be completed before Phase 4.")
            elif not phase4_done:
                # Pass necessary objects to phase_4
                phase_4(dataStorage, cleaned_df) # Pass the cleaned_df
                phase4_done = True
                print("✅ Phase 4 COMPLETED SUCCESSFULLY.")
            else:
                phase_4(dataStorage, cleaned_df) # Pass the cleaned_df
                print("✅ Phase 4 already completed. You can re-run it if needed.")



        elif choice == '0':
            print("👋 Exiting.")
            break

        else:
            print("❌ Invalid option or phase not unlocked yet.")


