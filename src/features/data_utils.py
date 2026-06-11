import re
import pandas as pd
from datetime import datetime
import numpy as np
import sys
sys.path.append('../') 
from features import general_func as gf

# Reading_Writing functions =========================================================
# Find the paitent folder in the data folder
def find_patient_folder(patients_data_folder: str, patient_id: str) -> dir:
    prefix = patient_id + "_"

    matching_dirs = [
        p for p in patients_data_folder.rglob("*")
        if p.is_dir() and p.name.lower().startswith(prefix.lower())
    ]

    current_patient_data_folder = matching_dirs[0] if matching_dirs else None

    return current_patient_data_folder

# Find the csv file in the folder
def find_csv_file(folder_path: str) -> list:
    
    csv_files = [
        file.name
        for file in folder_path.glob("*.csv")
    ]

    return csv_files

# Cleaning functions =========================================================
# Cleaning the csv file by removing the section breaks and merging the activity log into a single column
def cleaning_csv_file(csv_path_to_read: str, csv_path_to_write: str) -> None:
    
    with open(csv_path_to_read, "r", encoding="utf-8") as f:
        # 0. read all lines from the file
        lines = f.readlines()

    # 1. extract the first line (header) and split it into columns
    columns_line = lines[0]
    new_columns = columns_line.strip().split(",")
    lines.pop(0)  # remove the header line from the list of lines
    
    if (len(new_columns) != 10) and (len(new_columns) != 22):
        # remove spaces
        new_columns = [x for x in new_columns if x != ""]

    if len(new_columns) == 10: # add only for event files
        
        new_columns.append("Activity_Log") # add a new column for the Activity Log
    
    # 2. remove section breaks line and merge the Activity Log
    pattern = r"^--- SECTION BREAK:"
    rows = []

    for line in lines:

        if re.match(pattern, line):
            # skip lines like '--- SECTION BREAK:'
            continue

        elif not re.match(pattern, line):
            cleaned_line = cleaning_line(line, len(new_columns))

            rows.append(cleaned_line)

    #print(new_columns)
    df = pd.DataFrame(rows, columns=new_columns)
    
    return save_df(df, csv_path_to_write)
    
def cleaning_line(line: str, num_columns : int) -> list:

    messy_row = line.strip().split(",")

    if num_columns == 11:
            messy_row[10] = messy_row[10:] # merge all columns from index 10 onwards into a single column for the Activity Log
            del messy_row[11:] # delete the rest of them
    
    return messy_row

def save_df(df, csv_path):
    try:
        df.to_csv(csv_path, index=False)
        return True, None
    except Exception as e:
        return False, str(e)

# Extraction functions =========================================================
def extract_value_from_string(s:str, pattern_list:list) -> str | None:
    """
    Extracts a value from a string based on a provided regular expression pattern and converts it to the specified type.
    Args:
        s (str): The input string from which to extract the value.
        pattern (str): A regular expression pattern that defines how to extract the desired value from the string. The pattern should include a capturing group for the value to be extracted.
        type_to_extract (type): The type to which the extracted value should be converted. This can be int, float, or str.
    Returns:
        str | None: The extracted value converted (str), or None if the pattern does not match.
    """
  
    combined_patterns = '|'.join(pattern_list)
    
    matches = re.search(combined_patterns, s)
    
    if matches:
        return matches.group(1)
    else:
        None
    
def extract_phase_duration(df:pd.DataFrame)-> float:
    """
    Extracts the duration of a phase.
    Args:       
        df (pd.DataFrame): A DataFrame of one phase.
    Returns:        
        float: The duration of the phase in seconds, or None if the duration is none.
    """
    phase_duration = df[df['EventType']=='PHASE_END']['PhaseTime_s'].values[0] 
    return phase_duration

def extract_event_first_time(df: pd.DataFrame, events:list) -> float:
    """
    Extracts the time of the first time of an event from a DataFrame.
    Args:   
        df (pd.DataFrame): A DataFrame which should include 'EventType' and 'PhaseTime_s' columns.
    Returns:
        PhaseTime: Time in second for the first time that an event is occured.
    """
    PhaseTime = df[df['EventType'].isin(events)].iloc[0]['PhaseTime_s']
    return PhaseTime

# Calculation functions =========================================================
def calculate_duration_metric_stats(metric_series: pd.Series) -> tuple:
    """
    Calculates statistics for a given metric series.
    Args:
        metric_series (pd.Series): The series of metric values.
    Returns:
        tuple: A tuple containing the calculated statistics.
    """
    
    # calculate all statistics.
    total   = round(metric_series.sum(), 2)
    mean    = round(metric_series.mean(), 2)
    maximum = round(metric_series.max(), 2)
    median  = round(metric_series.median(), 2)
    std     = round(metric_series.std(), 2)

    """
    print("Mean:", mean)
    print("Max:", maximum)
    print("Median:", median)
    print("Std:", std)
    """
    return total, mean, maximum, median, std

def calculate_counting_metric_stats(metric_series: pd.Series) -> int:
    """
    Calculates statistics for a given metric series.
    Args:
        metric_series (pd.Series): The series of metric values.
    Returns:
        int: The calculated total sum.
    """

    # calculate total sum for both counting and duration metrics
    total = round(metric_series.sum(), 2)
    #print("Sum:", total)
    return total

def ratio_calculation(value1: float, value2: float) -> float:
    """
    Calculates the ratio of two values.
    Args:
        value1 (float): The numerator.
        value2 (float): The denominator.
    Returns:
        float: The calculated ratio, or None if the denominator is zero.
    """
    if value2 == 0:
        return None  # or you could return float('inf') to indicate an infinite ratio
    return round(value1 / value2, 2)

def calculate_decision_latency(first_hover_time: float, first_press_time: float) -> float:
    """
    Calculates the decision latency, which is the time difference in seconds between the first hover and the first press in a given section DataFrame.
    Args:
        first_hover_time (float): The time of the first hover event in seconds.
        first_press_time (float): The time of the first press event in seconds.
    Returns:
        float: The decision latency in seconds, or None if the timestamps cannot be parsed.
    """
    time_difference = round(first_press_time - first_hover_time, 2)
    return time_difference

def calculate_total_head_distance(df: pd.DataFrame) -> float:
    """
    Calculate total head movement by the distance of the three axis.
    Args:
        df(DataFrame): the trajectory file csv.
    Returns:
        float: the Total distance.
    """
    df['moved_distance'] = None

    for index in range(len(df)):
        
        if index == 0:
            df.loc[index, 'moved_distance'] = 0
            continue

        x = pow((df['HMD_X'].iloc[index-1] - df['HMD_X'].iloc[index]),2)
        y = pow((df['HMD_Y'].iloc[index-1] - df['HMD_Y'].iloc[index]),2)
        z = pow((df['HMD_Z'].iloc[index-1] - df['HMD_Z'].iloc[index]),2)

        moved_distance = np.sqrt(x+y+z)
        df.loc[index, 'moved_distance'] = round(moved_distance,2)

    total_distance = round(df['moved_distance'].sum(),2)
    return total_distance

def calculate_head_distance_speed_metrics(df: pd.DataFrame) -> tuple:
    df['head_distance_speed'] = None
    time_difference = None

    for index in range(len(df)):

        if index == 0:
            df.loc[index, 'head_distance_speed'] = 0
            continue

        time_difference = abs(df.loc[index, 'PhaseTime_s'] - df.loc[index-1, 'PhaseTime_s'])

        df.loc[index, 'head_distance_speed'] = df.loc[index, 'moved_distance'] / time_difference

    mean_head_speed = round(df['head_distance_speed'].mean(),2)
    max_head_speed  = round(df['head_distance_speed'].max(),2)
    std_head_speed  = round(df['head_distance_speed'].std(),2)

    return mean_head_speed, max_head_speed, std_head_speed

def calculate_total_head_orientation(df: pd.DataFrame) -> float:
    """
    Calculate total head orientation by the angle of the three axis.
    Args:
        df(DataFrame): the trajectory file csv.
    Returns:
        float: the Total orientation has taken.
    """
    df['moved_orientation'] = None

    for index in range(len(df)):
        
        if index == 0:
            df.loc[index, 'moved_orientation'] = 0
            continue

        yaw   = pow((df['HMD_Yaw'].iloc[index-1] - df['HMD_Yaw'].iloc[index]),2)
        pitch = pow((df['HMD_Pitch'].iloc[index-1] - df['HMD_Pitch'].iloc[index]),2)
        roll  = pow((df['HMD_Roll'].iloc[index-1] - df['HMD_Roll'].iloc[index]),2)

        moved_orientation = np.sqrt(yaw+pitch+roll)
        df.loc[index, 'moved_orientation'] = round(moved_orientation,2)

    total_orientation = round(df['moved_orientation'].sum(),2)
    return total_orientation

def calculate_head_orientation_speed_metrics(df: pd.DataFrame) -> tuple:
    
    df['head_orientation_speed'] = None
    time_difference = None

    for index in range(len(df)):

        if index == 0:
            df.loc[index, 'head_orientation_speed'] = 0
            continue

        time_difference = abs(df.loc[index, 'PhaseTime_s'] - df.loc[index-1, 'PhaseTime_s'])
        
        df.loc[index, 'head_orientation_speed'] = df.loc[index, 'moved_orientation'] / time_difference

    mean_head_speed = round(df['head_orientation_speed'].mean(),2)
    max_head_speed  = round(df['head_orientation_speed'].max(),2)
    std_head_speed  = round(df['head_orientation_speed'].std(),2)
    return mean_head_speed, max_head_speed, std_head_speed

def calculate_switch_count(df: pd.DataFrame) -> int:

    if (df['GazeTarget'].nunique() == 1) or (df['GazeTarget'].isna().all()):
        return 0

    else:
        objs = list(df['GazeTarget'].dropna().unique())
        current_obj  = objs[0]
        switch_count = 0

        for index in range(len(df)):
            if df.loc[index, 'GazeTarget']: # not none
                if current_obj != df.loc[index, 'GazeTarget']:
                    switch_count +=1
                    current_obj = df.loc[index, 'GazeTarget']

        return switch_count

def calculate_total_hand_distance(df: pd.DataFrame, hand: str) -> float:
    """
    Calculate total hand movement by the distance of the three axis.
    Args:
        df(DataFrame): the trajectory file csv.
    Returns:
        float: the Total distance.
    """
    name_column     = f'{hand}_moved_distance'
    df[name_column] = None

    for index in range(len(df)):
        
        if index == 0:
            df.loc[index, name_column] = 0
            continue

        x = pow((df[f'{hand}Ctrl_X'].iloc[index-1] - df[f'{hand}Ctrl_X'].iloc[index]),2)
        y = pow((df[f'{hand}Ctrl_Y'].iloc[index-1] - df[f'{hand}Ctrl_Y'].iloc[index]),2)
        z = pow((df[f'{hand}Ctrl_Z'].iloc[index-1] - df[f'{hand}Ctrl_Z'].iloc[index]),2)

        moved_distance = np.sqrt(x+y+z)
        df.loc[index, name_column] = round(moved_distance,2)

    total_distance = round(df[name_column].sum(),2)
    return total_distance

def calculate_hand_dinstance_speed_metrics(df: pd.DataFrame, hand: str) -> tuple:
    
    column_name     = f'{hand}_hand_distance_speed'
    df[column_name] = None
    time_difference = None

    for index in range(len(df)):

        if index == 0:
            df.loc[index, column_name] = 0
            continue

        time_difference = abs(df.loc[index, 'PhaseTime_s'] - df.loc[index-1, 'PhaseTime_s'])
        
        df.loc[index, column_name] = df.loc[index, f'{hand}_moved_distance'] / time_difference

    mean_hand_speed = round(df[column_name].mean(),2)
    max_hand_speed  = round(df[column_name].max(),2)

    return mean_hand_speed, max_hand_speed

def calculate_trigger_or_grip_hand_metrics(df: pd.DataFrame, hand: str, action: str) -> tuple:
    """
    Calculate metrics of hand Trigger or Grip (pressure mean and press count).
    Args:
        df(DataFrame): the trajectory file csv.
        hand(str) : Left or Right.
        action(str) : Trigger or Grip.
    Returns:
        tuple: pressure_mean, press_count
    """

    column_name = hand + action

    pressure_mean = round(df[column_name].mean(), 2) 
    press_count   = df[df[column_name]!= 0.0][column_name].size

    return press_count, pressure_mean

# Fill out dictionary function =========================================================
# Events
def filling_reading_time_dict(df: pd.DataFrame, reading_time_dict: dict, phase_duration: float) -> dict:

    # extracting
    reading_time_series = df['Activity_Log'].apply(extract_value_from_string,pattern_list=[r"ReadingTime=([0-9]*\.?[0-9]+)"])

    # cleaning
    reading_time_series = reading_time_series.dropna()
    reading_time_series = reading_time_series.astype(float)

    # filling dict
    reading_time_dict['total_reading_time'], reading_time_dict['mean_reading_time'], reading_time_dict['max_reading_time'], reading_time_dict['median_reading_time'], reading_time_dict['std_reading_time']= calculate_duration_metric_stats(metric_series=reading_time_series)

    reading_time_dict['intensity_reading_time'] = ratio_calculation(
                                                    value1=reading_time_dict['total_reading_time'],
                                                    value2=phase_duration
                                                    )

    # check none values
    has_none = any(value is None for value in reading_time_dict.values())

    if has_none:
        gf.fail(msg='None value found in reading_time_dict!!!', error='ValueError')

    return reading_time_dict

def filling_hover_dict(df: pd.DataFrame, hover_dict: dict, phase_duration: float)-> dict:
    
    patterns = [r"HoverCount=([0-9]+)", 
                r"TotalHovers=([0-9]+)"]

    # extracting and cleaning
    hover_series = df['Activity_Log'].apply(extract_value_from_string,pattern_list=patterns)
    hover_series = hover_series.dropna()
    hover_series = hover_series.astype(float)

    # filling
    hover_dict['total_count_hover'] = int(calculate_counting_metric_stats(metric_series=hover_series))

    patterns = [r"HoverDuration=([0-9]*\.?[0-9]+)"]

    # extracting and cleaning
    hover_series = df['Activity_Log'].apply(extract_value_from_string,pattern_list=patterns)
    hover_series = hover_series.dropna()
    hover_series = hover_series.astype(float)

    # filling
    hover_dict['total_duration_hover'], hover_dict['max_duration_hover'], hover_dict['mean_duration_hover'], hover_dict['median_duration_hover'], hover_dict['std_duration_hover'] = calculate_duration_metric_stats(metric_series=hover_series)

    # filling
    hover_dict['intensity_hover'] = round(hover_dict['total_duration_hover']/phase_duration,2)

    # check none values
    has_none = any(value is None for value in hover_dict.values())

    if has_none:
        gf.fail(msg='None value found in hover_dict!!!', error='ValueError')

    return hover_dict

def filling_press_dict(df: pd.DataFrame, press_dict: dict, phase_duration: float)-> dict:

    # extract
    press_df = df[df['EventType'].isin(['BUTTON_PRESSED','BUTTON_CLICKED'])]

    # filling
    press_dict['total_count_press']=len(press_df)

    # extract and cleaning
    patterns = [r"PressDuration=([0-9]*\.?[0-9]+)"]
    press_series = df['Activity_Log'].apply(extract_value_from_string,pattern_list=patterns)
    press_series = press_series.dropna()
    press_series = press_series.astype(float)

    # filling
    press_dict['total_duration_press'], press_dict['max_duration_press'], press_dict['mean_duration_press'], press_dict['median_duration_press'], press_dict['std_duration_press'] = calculate_duration_metric_stats(metric_series=press_series)

    # filling
    press_dict['intensity_press'] = round(press_dict['total_duration_press']/phase_duration,2)

    # check none values
    has_none = any(value is None for value in press_dict.values())

    if has_none:
        gf.fail(msg='None value found in press_dict!!!', error='ValueError')

    return press_dict

def filling_grab_dict(df: pd.DataFrame, grab_dict: dict, phase_duration: float)-> dict:

    # extract
    grab_df = df[df['EventType'].isin(['GRAB_RELEASE','GRAB_PRACTICE_PLACEMENT'])]

    # filling
    grab_dict['total_count_grab']=len(grab_df)
    
    # extract
    grab_series = df[df['EventType'].isin(['GRAB_RELEASE'])]['Duration_s']

    # filling
    grab_dict['total_duration_grab'], grab_dict['max_duration_grab'], grab_dict['mean_duration_grab'], grab_dict['median_duration_grab'], grab_dict['std_duration_grab'] = calculate_duration_metric_stats(metric_series=grab_series)
    grab_dict['intensity_grab'] = round(grab_dict['total_duration_grab']/phase_duration,2)

    # check none values
    has_none = any(value is None for value in grab_dict.values())

    if has_none:
        gf.fail(msg='None value found in grab_dict!!!', error='ValueError')

    return grab_dict

def filling_gaze_dict(df: pd.DataFrame, gaze_dict: dict, phase_duration: float)-> dict:

    # extract
    gaze_df = df[df['EventType'].isin(['GAZE_END'])]
    
    # filling
    gaze_dict['total_count_gaze'] = len(gaze_df)

    # extract and cleaning
    patterns = [r"DwellTime=([0-9]*\.?[0-9]+)"]
    gaze_series = df['Activity_Log'].apply(extract_value_from_string,pattern_list=patterns)
    gaze_series = gaze_series.dropna()
    gaze_series = gaze_series.astype(float)

    # filling
    gaze_dict['total_duration_gaze'], gaze_dict['max_duration_gaze'], gaze_dict['mean_duration_gaze'], gaze_dict['median_duration_gaze'], gaze_dict['std_duration_gaze'] = calculate_duration_metric_stats(metric_series=gaze_series)

    # filling
    gaze_dict['intensity_gaze'] = round(gaze_dict['total_duration_gaze']/phase_duration,2)

    # check none values
    has_none = any(value is None for value in gaze_dict.values())

    if has_none:
        gf.fail(msg='None value found in gaze_dict!!!', error='ValueError')

    return gaze_dict

def filling_behavior_dict(df: pd.DataFrame, behavior_dict: dict, hover_dict: dict, press_dict: dict, reading_time_dict: dict, phase_duration: float)-> dict:
    
    # extract
    first_hover_time = extract_event_first_time(df, ['BUTTON_HOVER_START'])
    first_press_time = extract_event_first_time(df, ['BUTTON_PRESSED','BUTTON_CLICKED'])

    # filling
    behavior_dict["hover_vs_active_interaction_ratio"] = ratio_calculation(hover_dict["total_duration_hover"], press_dict["total_duration_press"])
    behavior_dict["hover_vs_reading_time_ratio"]       = ratio_calculation(hover_dict["total_duration_hover"], reading_time_dict["total_reading_time"])
    behavior_dict["interaction_fraction"]              = ratio_calculation((hover_dict["total_duration_hover"] + press_dict["total_duration_press"]), phase_duration)
    behavior_dict["decision_latency"]                  = calculate_decision_latency(first_hover_time, first_press_time)
    behavior_dict["clicks_per_second"]                 = ratio_calculation(press_dict["total_count_press"], phase_duration)
    behavior_dict["hovers_per_click"]                  = ratio_calculation(hover_dict["total_count_hover"], press_dict["total_count_press"])

    # check none values
    has_none = any(value is None for value in behavior_dict.values())

    if has_none:
        gf.fail(msg='None value found in behavior_dict!!!', error='ValueError')

    return behavior_dict

def filling_temporal_dict(df: pd.DataFrame, temporal_dict: dict) -> dict:

    # extract
    first_hover_time = extract_event_first_time(df, ['BUTTON_HOVER_START'])
    first_press_time = extract_event_first_time(df, ['BUTTON_PRESSED','BUTTON_CLICKED'])

    # filling
    temporal_dict['time_before_first_press'] = first_press_time
    temporal_dict['time_before_first_hover'] = first_hover_time

    # check none values
    has_none = any(value is None for value in temporal_dict.values())

    if has_none:
        gf.fail(msg='None value found in temporal_dict!!!', error='ValueError')

    return temporal_dict

def filling_obj_recognition_dict(df: pd.DataFrame, obj_recognition:dict) -> dict:

    # initial
    total_successful_round = 0
    arr_success_duration   = np.array([])
    arr_choose_wrong_obj   = np.array([])

    # extract
    patterns  = [r"TotalRounds=([0-9]+)"]
    round_num = df[df['EventType']=='GAME_START']['Activity_Log'].apply(extract_value_from_string, pattern_list=patterns)

    round_num = int(round_num.iloc[0])

    # extract and calculate for each round
    for value in range(round_num):
        
        round_name = f'Round{value+1}'

        start_index = df[(df['Section'] == round_name) & (df['EventType'] == 'SECTION_START')].index
        end_index   = df[(df['Section'] == round_name) & (df['EventType'] == 'SECTION_END')].index

        if (len(start_index) != 1) and (len(end_index) != 1):
            raise ValueError("More than 1 start or end index!!!")
        
        round_df = df.iloc[start_index[0]:end_index[0]]

        # feautre 1 : 
        is_successful = 'SELECTION_CORRECT' in round_df['EventType'].values

        # feature 2:
        if is_successful:
            total_successful_round += 1

            success_duration = round_df[round_df['EventType']=='SELECTION_CORRECT']['Duration_s'].iloc[0]
            arr_success_duration = np.append(arr_success_duration, success_duration)
        
        else:
            success_duration = None

        # feature 3:
        patterns = [r"IsCorrect=([^\W]+)"]
        round_series = round_df['Activity_Log'].apply(extract_value_from_string,pattern_list=patterns)
        num_wrong_obj_chosen = (round_series == 'False').sum()

        arr_choose_wrong_obj = np.append(arr_choose_wrong_obj, num_wrong_obj_chosen)

    # filling
    obj_recognition["obj_recognition_score"] = ratio_calculation(value1 = total_successful_round, value2 = round_num)
    obj_recognition["obj_recognition_mean_success_duration"]  = round(np.mean(arr_success_duration), 2)
    obj_recognition["obj_recognition_mean_choose_wrong_obj"]  = round(np.mean(arr_choose_wrong_obj), 2)

    # extract 
    game_start_time  = df[(df['Section'] == 'Initial') & (df['EventType'] == 'GAME_START')]['PhaseTime_s'].iloc[0]
    game_finish_time = df[(df['Section'] == 'Summary') & (df['EventType'] == 'GAME_COMPLETE')]['PhaseTime_s'].iloc[0]
    
    total_duration = diff if (diff := game_finish_time - game_start_time) > 0 else sys.exit("game timer is not valid!!!")
    
    # filling
    obj_recognition["obj_recognition_total_duration"] = total_duration

    # check none values
    has_none = any(value is None for value in obj_recognition.values())

    if has_none:
        gf.fail(msg='None value found in obj_recognition!!!', error='ValueError')

    return obj_recognition

def filling_visuospatial_dict(df: pd.DataFrame, visuospatial_dict) -> dict:

    # extracting
    string_activity_log = df[(df['Section'] == 'Completion') & (df['EventType'] == 'VISUOSPATIAL_COMPLETE')]['Activity_Log'].iloc[0]
    total_time_string = extract_value_from_string(string_activity_log, pattern_list=[r"Time=([0-9]*\.?[0-9]+)"])

    # filling
    visuospatial_dict["visuospatial_total_duration"] = float(total_time_string)

    # extracting
    string_activity_log   = df[(df['Section'] == 'Completion') & (df['EventType'] == 'VISUOSPATIAL_COMPLETE')]['Activity_Log'].iloc[0]
    num_correct_placement = extract_value_from_string(string_activity_log, pattern_list=[r"Correct=([0-9]+)"])
    num_total_object      = extract_value_from_string(string_activity_log, pattern_list=[r"Total=([0-9]+)"])

    # filling
    visuospatial_dict["visuospatial_score"] = ratio_calculation(value1=float(num_correct_placement), value2=float(num_total_object))

    # filling
    visuospatial_dict["visuospatial_total_wrong_placement"] = (df['EventType'] == "SOCKET_REJECTION").sum()

    # check none values
    has_none = any(value is None for value in visuospatial_dict.values())

    if has_none:
        gf.fail(msg='None value found in visuospatial_dict!!!', error='ValueError')

    return visuospatial_dict

def filling_memory_dict(df: pd.DataFrame, memory_dict) -> dict:
    
    # extract
    string_activity_log   = df[(df['Section'] == 'Completion') & (df['EventType'] == 'MEMORY_COMPLETE')]['Activity_Log'].iloc[0]
    num_correct_placement = extract_value_from_string(string_activity_log, pattern_list=[r"Correct=([0-9]+)"])
    num_total_object      = extract_value_from_string(string_activity_log, pattern_list=[r"Total=([0-9]+)"])

    # filling
    memory_dict["memory_score"] = ratio_calculation(value1=float(num_correct_placement), value2=float(num_total_object))

    # extract
    string_activity_log =  df[df['EventType'] == 'RECALL_FIRST_ACTION']['Activity_Log'].iloc[0]

    # filling
    memory_dict["memory_delay_first_action"] = extract_value_from_string(string_activity_log, pattern_list=[r"DelayFromPhaseStart=([0-9]*\.?[0-9]+)"])

    # filling
    memory_dict["memory_total_wrong_recall"] = len(df[df['EventType'] == 'SOCKET_REJECTION'])

    # fillling
    memory_dict["memory_mean_recall"] = round(df[(df['EventType'] == 'MEMORY_RECALL')]['Duration_s'].mean(), 2)

    # extract
    string_activity_log = df[df['EventType'] == 'MEMORY_COMPLETE']['Activity_Log'].iloc[0]

    # filling
    memory_dict["memory_total_duration" ] = extract_value_from_string(string_activity_log, pattern_list=[r"RecallTime=([0-9]*\.?[0-9]+)"])

    memory_dict["memory_cognitive_freez_count"] = len(df[df['EventType'] == 'COGNITIVE_FREEZE'])

    # extract and clean
    freeze_series = df['Activity_Log'].apply(extract_value_from_string,pattern_list=[r"FreezeDuration=([0-9]*\.?[0-9]+)"])
    freeze_series = freeze_series.dropna()
    freeze_series = freeze_series.astype(float)

    # filling
    memory_dict["memory_cognitive_freez_mean_duration"] = freeze_series.mean()

    # check none values
    has_none = any(value is None for value in memory_dict.values())

    if has_none:
        gf.fail(msg='None value found in memory_dict!!!', error='ValueError')

    return memory_dict

# Trajectory
def filling_headset_dict(df: pd.DataFrame, headset_dict: dict) -> dict:
    # filling distance features
    headset_dict['head_total_distance'] = calculate_total_head_distance(df)

    headset_dict['HMD_X_std'] = round(df['HMD_X'].std(),2)
    headset_dict['HMD_Y_std'] = round(df['HMD_Y'].std(),2)
    headset_dict['HMD_Z_std'] = round(df['HMD_Z'].std(),2)

    headset_dict['HMD_X_range'] = round(df['HMD_X'].max() - df['HMD_X'].min(),2)
    headset_dict['HMD_Y_range'] = round(df['HMD_Y'].max() - df['HMD_Y'].min(),2)
    headset_dict['HMD_Z_range'] = round(df['HMD_Z'].max() - df['HMD_Z'].min(),2)

    headset_dict['mean_head_speed_in_distance'], headset_dict['max_head_speed_in_distance'], headset_dict['std_head_speed_in_distance'] = calculate_head_distance_speed_metrics(df)

    # filling orientation features
    headset_dict["head_total_orientation"] = calculate_total_head_orientation(df)
    
    headset_dict['Yaw_std']   = round(df['HMD_Yaw'].std(),2)
    headset_dict['Pitch_std'] = round(df['HMD_Pitch'].std(),2)
    headset_dict['Roll_std']  = round(df['HMD_Roll'].std(),2)

    headset_dict['Yaw_range']   = round(df['HMD_Yaw'].max() - df['HMD_Yaw'].min(),2)
    headset_dict['Pitch_range'] = round(df['HMD_Pitch'].max() - df['HMD_Pitch'].min(),2)
    headset_dict['Roll_range']  = round(df['HMD_Roll'].max() - df['HMD_Roll'].min(),2)

    headset_dict['mean_head_speed_in_orientation'], headset_dict['max_head_speed_in_orientation'], headset_dict['std_head_speed_in_orientation'] = calculate_head_orientation_speed_metrics(df)

    # extract
    not_none_GazeTarget = df['GazeTarget'].notna().sum()

    # filling gaze features
    headset_dict['gaze_obj_looked_ratio'] = ratio_calculation(not_none_GazeTarget,len(df))

    headset_dict['gaze_switch_count'] = calculate_switch_count(df)

    # check none values
    has_none = any(value is None for value in headset_dict.values())

    if has_none:
        print(headset_dict)
        gf.fail(msg='None value found in headset_dict!!!', error='ValueError')

    return headset_dict

def filling_controller_dict(df: pd.DataFrame, dominant_hand: str, not_dominant_hand:str , controller_dict: dict)-> dict:
    
    # filling distance features
    controller_dict["dominant_hand_total_distance"]     = calculate_total_hand_distance(df,dominant_hand)
    controller_dict["not_dominant_hand_total_distance"] = calculate_total_hand_distance(df,not_dominant_hand)

    controller_dict["dominant_hand_mean_speed"], controller_dict["dominant_hand_max_speed"]         = calculate_hand_dinstance_speed_metrics(df, dominant_hand)
    controller_dict["not_dominant_hand_mean_speed"], controller_dict["not_dominant_hand_max_speed"] = calculate_hand_dinstance_speed_metrics(df, not_dominant_hand)

    controller_dict['dominant_hand_x_range']     = round(df[f'{dominant_hand}Ctrl_X'].max() - df[f'{dominant_hand}Ctrl_X'].min(),2)
    controller_dict['dominant_hand_y_range']     = round(df[f'{dominant_hand}Ctrl_Y'].max() - df[f'{dominant_hand}Ctrl_Y'].min(),2)
    controller_dict['dominant_hand_z_range']     = round(df[f'{dominant_hand}Ctrl_Z'].max() - df[f'{dominant_hand}Ctrl_Z'].min(),2)

    controller_dict['not_dominant_hand_x_range'] = round(df[f'{not_dominant_hand}Ctrl_X'].max() - df[f'{not_dominant_hand}Ctrl_X'].min(),2)
    controller_dict['not_dominant_hand_y_range'] = round(df[f'{not_dominant_hand}Ctrl_Y'].max() - df[f'{not_dominant_hand}Ctrl_Y'].min(),2)
    controller_dict['not_dominant_hand_z_range'] = round(df[f'{not_dominant_hand}Ctrl_Z'].max() - df[f'{not_dominant_hand}Ctrl_Z'].min(),2)

    # filling trigger features
    controller_dict["dominant_hand_trigger_press_count"], controller_dict["dominant_hand_trigger_pressure_mean"]         = calculate_trigger_or_grip_hand_metrics(df, dominant_hand, 'Trigger')
    controller_dict["not_dominant_hand_trigger_press_count"], controller_dict["not_dominant_hand_trigger_pressure_mean"] = calculate_trigger_or_grip_hand_metrics(df, not_dominant_hand, 'Trigger')

    # filling grip features
    controller_dict["dominant_hand_grip_count"], controller_dict["dominant_hand_grip_mean"] = calculate_trigger_or_grip_hand_metrics(df, dominant_hand, 'Grip')
    controller_dict["not_dominant_hand_grip_count"], controller_dict["not_dominant_hand_grip_mean"]= calculate_trigger_or_grip_hand_metrics(df, not_dominant_hand, 'Grip')

    # check none values
    has_none = any(value is None for value in controller_dict.values())

    if has_none:
        gf.fail(msg='None value found in controller_dict!!!', error='ValueError')

    return controller_dict

def filling_patient_dict(df: pd.DataFrame, paitent_dict: dict, row_index: int)-> dict:

    paitent_dict["Paitent_id"] = df.iloc[row_index]['PatientID']
    paitent_dict["Age"]        = df.iloc[row_index]['Age']
    paitent_dict["Gender"]     = df.iloc[row_index]['Gender']
    paitent_dict["dominant_hand"]     = df.iloc[row_index]['dominant_hand']
    paitent_dict["Sessions_Completed_out_of_4"] = df.iloc[row_index]['Sessions_Completed_out_of_4']
    paitent_dict["Help_Rating_out_of_5"]        = df.iloc[row_index]['Help_Rating_out_of_5']

    # check none values
    has_none = any(value is None for value in paitent_dict.values())

    if has_none:
        gf.fail(msg='None value found in paitent_dict!!!', error='ValueError')

    return paitent_dict