import re
import pandas as pd
from datetime import datetime

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

    if len(new_columns) == 10:
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
def extract_value_from_string(s:str, pattern_list:list, type_to_extract: type) -> list | None:
    """
    Extracts a value from a string based on a provided regular expression pattern and converts it to the specified type.
    Args:
        s (str): The input string from which to extract the value.
        pattern (str): A regular expression pattern that defines how to extract the desired value from the string. The pattern should include a capturing group for the value to be extracted.
        type_to_extract (type): The type to which the extracted value should be converted. This can be int, float, or str.
    Returns:
        list | None: The extracted value converted to the specified type, or None if the pattern does not match or if the type conversion fails.
    """
    combined_patterns = '|'.join(pattern_list)
    
    matches = re.search(combined_patterns, s)
    
    
    if matches: 
        if type_to_extract == int:
            return int(matches.group(1))
        elif type_to_extract == float:
            return float(matches.group(1))
        else:
            return matches.group(1)
    else:
        return None

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
    total = round(metric_series.sum(), 2)
    mean = round(metric_series.mean(), 2)
    maximum = round(metric_series.max(), 2)
    median = round(metric_series.median(), 2)
    std = round(metric_series.std(), 2)

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
    time_difference = first_press_time - first_hover_time
    return time_difference

# Fill out dictionary function =========================================================