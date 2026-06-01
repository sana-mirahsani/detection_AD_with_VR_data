import re
import pandas as pd
from datetime import datetime

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

# Filtering functions ========================================================
def filter_on_section(df: pd.DataFrame, section_name: str) -> pd.DataFrame:
    """
    Extracts rows from the DataFrame that belong to a specific section.
    Args:        
        df (pd.DataFrame): The input DataFrame containing the data.
        section_name (str): The name of the section to extract.
    Returns:        
        pd.DataFrame: A DataFrame containing only the rows that belong to the specified section.
    """
    df_with_one_section = df[df['Section'] == section_name]
    return df_with_one_section

def filter_by_string_contains(df: pd.DataFrame, column_name: str, substring: str) -> pd.DataFrame:
    """
    Filters the DataFrame to include only rows where the specified column contains a given substring.
    Args:
        df (pd.DataFrame): The input DataFrame to filter.
        column_name (str): The name of the column to check for the substring.
        substring (str): The substring to look for within the specified column.
    Returns:
        pd.DataFrame: A DataFrame containing only the rows where the specified column contains the given substring.
    """
    return df[df[column_name].str.contains(substring, na=False)]

# Extraction functions =========================================================
def extract_section_duration(s: str)-> float:
    """
    Extracts the duration of a section from Activity log of event_type == section_end.
    Args:       
        s (str): A string that contains the section end information.
    Returns:        
        float: The duration of the section in seconds, or None if the duration cannot be extracted
    """
    match = re.search(r"Duration=([0-9]*\.?[0-9]+)", s)
    return float(match.group(1)) if match else None

def extract_hover_count(s: str)-> int:
    """
    Extracts the hover count from a string of Activity_Log that contains the hover information.
    Args:       
        s (str): Value of Activity_Log columns that contains the hover information of HoverCount=
    Returns:
        int: The hover count, or None if the hover count cannot be extracted"""
    
    match = re.search(r"HoverCount=(\d+)", s)
    return int(match.group(1)) if match else None

def extract_hover_duration(s: str)-> float:
    """
    Extracts the hover duration from a string of Activity_Log that contains the hover information.
    Args:       
        s (str): Value of Activity_Log columns that contains the hover information of HoverDuration=
    Returns:
        float: The hover duration, or None if the hover duration cannot be extracted."""
    
    match = re.search(r"HoverDuration=([0-9]*\.?[0-9]+)", s)
    return float(match.group(1)) if match else None

def extract_press_duration(s: str)-> float:
    """
    Extracts the press duration from a string of Activity_Log that contains the press information.
    Args:
        s (str): Value of Activity_Log columns that contains the press information of PressDuration=
    Returns:
        float: The press duration, or None if the press duration cannot be extracted."""
    
    match = re.search(r"PressDuration=([0-9]*\.?[0-9]+)", s)
    return float(match.group(1)) if match else None

def extract_reading_time_duration(s: str)-> float:
    """
    Extracts the reading time duration from a string of Activity_Log that contains the reading time information.
    Args:
        s (str): Value of Activity_Log columns that contains the reading time information of ReadingTime=
    Returns:
        float: The reading time duration, or None if the reading time duration cannot be extracted."""
    
    match = re.search(r"ReadingTime=([0-9]*\.?[0-9]+)", s)
    return float(match.group(1)) if match else None

def extract_metric_from_section(filtered_df: pd.DataFrame, function_to_extract_metric: callable) -> pd.Series:
    """
    Extracts a specific metric from the 'Activity_Log' column of a filtered DataFrame using a provided extraction function.
    Args:
        filtered_df (pd.DataFrame): A DataFrame that has been filtered to contain only the relevant section.
        function_to_extract_metric (callable): A function that takes a string as input and extracts the desired metric from it.
    Returns:
        pd.Series: A pandas Series containing the extracted metric values for each row in the filtered Data
    """
    section_metric_values = []
    for value in filtered_df['Activity_Log']:
        #print(function_to_extract_metric(value))
        section_metric_values.append(function_to_extract_metric(value))

    section_metric_values_pandas = pd.Series(section_metric_values)
    return section_metric_values_pandas

def extract_first_time_hover(section_df: pd.DataFrame) -> float:
    """
    Extracts the time of the first hover event from a section DataFrame.
    Args:   
        section_df (pd.DataFrame): A DataFrame containing the data for a specific section, which should include 'EventType' and 'PhaseTime_s' columns.
    Returns:
        pd.Series: A pandas Series containing the time of the first hover event in seconds, or
    """
    first_hover_time = section_df[section_df['EventType'] == 'BUTTON_HOVER_START'].iloc[0]['PhaseTime_s']
    return first_hover_time

def extract_first_time_press(section_df: pd.DataFrame) -> float:
    """
    Extracts the time of the first click event from a section DataFrame.
    Args:   
        section_df (pd.DataFrame): A DataFrame containing the data for a specific section, which should include 'EventType' and 'PhaseTime_s' columns.
    Returns:
        pd.Series: A pandas Series containing the time of the first click event in seconds, or None if there are no click events.
    """
    first_click_time = section_df[section_df['EventType'] == 'BUTTON_PRESSED'].iloc[0]['PhaseTime_s']
    return first_click_time

# Calculation functions =========================================================
def calculate_metric_stats(metric_series: pd.Series, is_counting: bool=True) -> tuple:
    """
    Calculates statistics for a given metric series.
    Args:
        metric_series (pd.Series): The series of metric values.
        is_counting (bool): Whether the metric is a count (True) or duration (False).
    Returns:
        tuple: A tuple containing the calculated statistics.
    """
    # calculate total sum for both counting and duration metrics
    total = round(metric_series.sum(),2)
    #print("Sum:", total)

    # For counting metrics, we only care about the total sum.
    if is_counting:
        total = metric_series.sum()
        return total, None, None, None, None
    
    # For duration metrics, we calculate all statistics.
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