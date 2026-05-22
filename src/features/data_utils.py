import re
import pandas as pd

def creating_sections_of_csv(file_path_to_read: str, file_path_to_write: str) -> None:

    with open(file_path_to_read, "r", encoding="utf-8") as f:
        # 0. read all lines from the file
        lines = f.readlines()

    # 1. extract the first line (header) and split it into columns
    columns_line = lines[0]
    new_columns = columns_line.strip().split(",")
    lines.pop(0)  # remove the header line from the list of lines
    new_columns.append("Activity_Log") # add a new column for the Activity Log

    # 2. separate lines based on the section break
    pattern = r"^--- SECTION BREAK:"
    section_lines = []
    section_name = None

    for line in lines:
        if re.match(pattern, line):
            cleaned_section_lines = cleaning_section_lines(section_lines)
            df = pd.DataFrame(cleaned_section_lines, columns=new_columns)
            
            if df['Section'].nunique() == 1:
                section_name = df['Section'].unique()[0]
                file_path_to_write = f'../../data/cleaned_data_{section_name}.csv'

                # Save the cleaned DataFrame to a new CSV file
                df.to_csv(file_path_to_write, index=False)
                
                # Reset section_lines for the next section
                section_lines = []

            else:
                raise ValueError("Multiple sections found in the same section break. Please check the data.")

            continue  # skip the section break line itself

        section_lines.append(line)


def cleaning_section_lines(section_lines: list) -> list:
    cleaned_section_lines = []

    for line in section_lines:
        messy_row = line.strip().split(",")
        messy_row[10] = messy_row[10:] # merge all columns from index 10 onwards into a single column for the Activity Log
        del messy_row[11:] # delete the rest of them
        cleaned_section_lines.append(messy_row)

    return cleaned_section_lines