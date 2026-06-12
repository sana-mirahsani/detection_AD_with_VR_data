from features import data_utils
from pathlib import Path
import pandas as pd
import sys

sys.path.append('../') 
from features import data_utils as du
from features import general_func as gf

# piple for cleaning functions
def pipeline_cleaning(list_patient_id: list,
                      patients_data_folder: str) -> None:
    """
    cleaning process, removing Section Break rows and add Activity Log column as the last row.
    Args: 
        list_patient_id(List): All ids of patients as a list.
        patients_data_folder(str): Path of data folder.
    Returns:
        None: check the directory, must see a new folder called clean_data.
    """
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

# Pipeline for creating feature vectors
def creating_event_dictionary(df: pd.DataFrame, phase_name: str, empty_dictionaries:list, extra_features_empty_dictionaries:list, phase_duration:float) -> dict:
    """
    Filling all eventy features (basics and extra features for other phases)
    Args: 
        df(Dataframe): trajectory csv
        phase_name(str): Tutorial or ObjectRecognition or Visuospatial or Memory.
        empty_dictionaries(list): list of basic dictionaries (empty at first).
        extra_features_dictionaries(List): list of 3 extra feature dictionary (empty at first).
        phase_dict(dict): dictionary of phase (for each 4 phases and not empty!).
    Returns:
        concated all basic dictionaries (also with extra features depends on phase name) as the event dict.
    """
    # filling read_time dict
    reading_time_dict = du.filling_reading_time_dict(df, empty_dictionaries[0], phase_duration)
    
    # filling hover_dict
    hover_dict = du.filling_hover_dict(df, empty_dictionaries[1], phase_duration)

    # filling press_dict
    press_dict = du.filling_press_dict(df, empty_dictionaries[2], phase_duration)

    # filling grab_dict
    grab_dict = du.filling_grab_dict(df, empty_dictionaries[3], phase_duration)

    # filling gaze_dict
    gaze_dict = du.filling_gaze_dict(df, empty_dictionaries[4], phase_duration)

    # filling behavior_dict
    behavior_dict = du.filling_behavior_dict(df, empty_dictionaries[5], hover_dict, press_dict, reading_time_dict, phase_duration)

    # filling temporal_dict
    temporal_dict = du.filling_temporal_dict(df, empty_dictionaries[6])

    # concate all dictionaries
    event_dictionary = reading_time_dict | hover_dict | press_dict | grab_dict | gaze_dict | behavior_dict | temporal_dict

    # check for extra features
    match phase_name:

        case 'Tutorial':
            return event_dictionary
        
        case 'ObjectRecognition':

            obj_recognition_dict = extra_features_empty_dictionaries[0]

            # fill and add extra features to basic dict
            obj_recognition_dict = du.filling_obj_recognition_dict(df, obj_recognition_dict)
            event_dictionary.update(obj_recognition_dict)

            return event_dictionary
        
        case 'Visuospatial':
            
            visuospatial_dict = extra_features_empty_dictionaries[1]

            # fill and add extra features to basic dict
            visuospatial_dict = du.filling_visuospatial_dict(df, visuospatial_dict)
            event_dictionary.update(visuospatial_dict)
            
            return event_dictionary
        
        case 'Memory':

            memory_dict = extra_features_empty_dictionaries[2]

            # fill and add extra features to basic dict
            memory_dict = du.filling_memory_dict(df, memory_dict)
            event_dictionary.update(memory_dict)
            
            return event_dictionary
        
        case _ :
            gf.fail(msg="not valid value for test_name!!!", error="ValueError")

def creating_trajectory_dictionary(df: pd.DataFrame, dominant_hand: str, not_dominant_hand: str, empty_dictionaries:list) -> dict:
    """
    Filling all trajectory features (headset and controller)
    Args: 
        df(Dataframe): trajectory csv
        dominant_hand(str): dominant hand of patient.
        not_dominant_hand(str): dominant hand of patient.
        empty_dictionaries(List): headset and controler dictionary but empty.
    Returns:
        concated headset_dict and controler_dict as the trajectory dict.
    """
    # fill headset dictionary
    headset_dict = du.filling_headset_dict(df, empty_dictionaries[0])

    # fill controler dictionary
    controler_dict = du.filling_controller_dict(df, dominant_hand, not_dominant_hand, empty_dictionaries[0])

    # concate all dictionaries
    trajectory_dictionary = headset_dict | controler_dict

    # check dict
    gf.general_dict_check(trajectory_dictionary, "trajectory_dictionary", None)
    
    return trajectory_dictionary