from features import data_utils
from pathlib import Path
import pandas as pd
import sys
sys.path.append('../') 
from features import data_utils as du

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

def creating_feature_vector_section_default(section_default_df: pd.DataFrame,
                                            hover_dict: dict,
                                            press_dict: dict,
                                            reading_time_dict: dict,
                                            behavior_dict: dict,
                                            temporal_dict: dict) -> pd.DataFrame: 

    features_dict = {
        "section_id": None,
        "section_name": None,
        "section_total_time": None,
    }
    
    # extract section duration
    row_section_end = section_default_df[section_default_df['EventType']=='SECTION_END']['Activity_Log'].values[0]
    section_total_time = du.extract_section_duration(row_section_end)

    # fill out hover_dict
    # hover count
    filtered_df = du.filter_by_string_contains(section_default_df, 'Activity_Log', 'HoverCount')
    hover_count_series = du.extract_metric_from_section(filtered_df, du.extract_hover_count)
    hover_dict["total_hover_count"], _ , _ , _ , _ = du.calculate_metric_stats(hover_count_series, is_counting=True)

    # hover duration
    filtered_df = du.filter_by_string_contains(section_default_df, 'Activity_Log', 'HoverDuration')
    hover_duration_series = du.extract_metric_from_section(filtered_df, du.extract_hover_duration)
    hover_dict["total_hover_duration"], hover_dict["mean_hover_duration"], hover_dict["max_hover_duration"], hover_dict["median_hover_duration"], hover_dict["std_hover_duration"] = du.calculate_metric_stats(hover_duration_series, is_counting=False)

    # hover intensity
    hover_dict["hover_intensity"] = du.ratio_calculation(hover_dict["total_hover_duration"], section_total_time)

    # hover cv (Coefficient of Variation)
    hover_dict["cv_hover_duration"] = du.ratio_calculation(hover_dict["std_hover_duration"], hover_dict["mean_hover_duration"])

    # fill out press_dict
    # press count (assumed that for each button pressed, there is a button released too
    filtered_df_button_pressed = du.filter_by_string_contains(section_default_df, 'EventType', 'BUTTON_PRESSED')
    total_press_count = len(filtered_df_button_pressed)  # Assuming each press has a corresponding release
    press_dict["total_press_count"] = total_press_count

    # press duration
    filtered_df = du.filter_by_string_contains(section_default_df, 'Activity_Log', 'PressDuration')
    press_duration_series = du.extract_metric_from_section(filtered_df, du.extract_press_duration)

    press_dict["total_press_duration"], press_dict["mean_press_duration"], press_dict["max_press_duration"], press_dict["median_press_duration"], press_dict["std_press_duration"] = du.calculate_metric_stats(press_duration_series, is_counting=False)

    # press_intensity
    press_dict["press_intensity"] = du.ratio_calculation(press_dict["total_press_duration"], section_total_time)

    # fill out reading_time_dict
    # reading time duration
    filtered_df = du.filter_by_string_contains(section_default_df, 'Activity_Log', 'ReadingTime')
    reading_time_series = du.extract_metric_from_section(filtered_df, du.extract_reading_time_duration)

    # calculation for reading time duration
    reading_time_dict["total_reading_time_duration"], reading_time_dict["mean_reading_time_duration"], reading_time_dict["max_reading_time_duration"], reading_time_dict["median_reading_time_duration"], reading_time_dict["std_reading_time_duration"] = du.calculate_metric_stats(reading_time_series, is_counting=False)

    # reading time intensity
    reading_time_dict["reading_time_intensity"] = du.ratio_calculation(reading_time_dict["total_reading_time_duration"], section_total_time)

    # fill out behavior_dict
    behavior_dict["hover_vs_active_interaction_ratio"] = du.ratio_calculation(hover_dict["total_hover_duration"], press_dict["total_press_duration"])
    behavior_dict["hover_vs_reading_time_ratio"] = du.ratio_calculation(hover_dict["total_hover_duration"], reading_time_dict["total_reading_time_duration"])

    behavior_dict["interaction_fraction"] = du.ratio_calculation(hover_dict["total_hover_duration"] + press_dict["total_press_duration"], section_total_time)

    behavior_dict["decision_latency"] = du.calculate_decision_latency(first_hover_time=du.extract_first_time_hover(section_default_df), first_press_time=du.extract_first_time_press(section_default_df))

    behavior_dict["clicks_per_second"] = du.ratio_calculation(press_dict["total_press_count"], section_total_time)
    behavior_dict["hovers_per_click"] = du.ratio_calculation(hover_dict["total_hover_count"], press_dict["total_press_count"])

    # fill out temproal_dict
    temporal_dict['time_before_first_press'] = du.extract_first_time_press(section_default_df)
    temporal_dict['time_before_first_hover'] = du.extract_first_time_hover(section_default_df)

    # create dataframe
    features_dict["section_id"] = 1
    features_dict["section_name"] = 'Default'
    features_dict["section_total_time"] = section_total_time

    features_dict.update(hover_dict)
    features_dict.update(press_dict)
    features_dict.update(reading_time_dict)
    features_dict.update(behavior_dict)
    features_dict.update(temporal_dict)

    return pd.DataFrame([features_dict])

def creating_feature_vector_tutorial_events():pass