import re
import pandas as pd

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

# feature extraction of tutorial events
def extract_section(df: pd.DataFrame, section_name: str) -> pd.DataFrame:
    df_with_one_section = df[df['Section'] == section_name]
    return df_with_one_section

def extract_event_types(df : pd.DataFrame, events_to_ignore: list) -> list:
    event_types = df['EventType'].unique()
    return [event for event in event_types if event not in events_to_ignore]

#def extract_dict_hover_button