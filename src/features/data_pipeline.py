from features import data_utils
from pathlib import Path

def pipeline_cleaning(list_patient_id: list,
                      patients_data_folder: str) -> None:
    
    print("Starting the data cleaning pipeline...")

    for patient_id in list_patient_id:
        print(f"Processing patient ID: {patient_id}")
        
        current_patient_data_folder = data_utils.find_patient_folder(patients_data_folder, patient_id)

        if current_patient_data_folder is None:
            print(f"Patient folder not found for ID: {patient_id} !!!!!!!!!")
            continue

        list_of_csv_files = data_utils.find_csv_file(folder_path=current_patient_data_folder)
        
        for csv_file in list_of_csv_files:
            
            if "_SESSION_SUMMARY" in csv_file:
                continue  # skip this file

            input_path_of_csv = current_patient_data_folder / csv_file
            
            Path(current_patient_data_folder / "clean_data").mkdir(exist_ok=True)
            
            output_path_of_csv = current_patient_data_folder / 'clean_data' / f"cleaned_{csv_file}"

            success, error = data_utils.cleaning_csv_file(csv_path_to_read=input_path_of_csv, 
                                        csv_path_to_write=output_path_of_csv)
            if not success:
                print(f"Error: {error}")
                raise FileNotFoundError("There was an error in saving the csv file.")
            
        print("Cleaning OK, next patient...")
    print("Cleaning process completed.")