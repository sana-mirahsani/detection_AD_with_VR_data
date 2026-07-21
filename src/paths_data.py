from pathlib import Path
import pandas as pd

# Root of the project
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Main Data folders
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
INTERIM_DATA_DIR = DATA_DIR / "interim"
PREDICTIONS_DIR = DATA_DIR / "predictions"

# Sub Data Folder
STAGE_ONE_BASIC_CLEANING       = INTERIM_DATA_DIR / "stage_one_basic_cleaning"
STAGE_TWO_FEATURE_EXTRACTION   = INTERIM_DATA_DIR / "stage_two_feature_extraction"
STAGE_THREE_DATA_PREPROCESSING = INTERIM_DATA_DIR / "stage_three_data_preprocessing"

COLUMNS_TO_REMOVE =  INTERIM_DATA_DIR / "columns_to_remove.txt"

PREDICTS_SOLTUION_ONE   =  PREDICTIONS_DIR / "predicts_sol_one"
PREDICTS_SOLTUION_TWO   =  PREDICTIONS_DIR / "predicts_sol_two"
PREDICTS_SOLTUION_THREE =  PREDICTIONS_DIR / "predicts_sol_three"

# Models
MODELS_DIR_SOL_ONE   = PROJECT_ROOT / "models" / "solution_one"
MODELS_DIR_SOL_TWO   = PROJECT_ROOT / "models" / "solution_two"
MODELS_DIR_SOL_THREE = PROJECT_ROOT / "models" / "solution_three"

# Results
RESULTS_DIR = PROJECT_ROOT / "results_and_figures"

# Create directories if they don't exist
for folder in [
    RAW_DATA_DIR,
    INTERIM_DATA_DIR,
    PREDICTIONS_DIR,
    STAGE_ONE_BASIC_CLEANING,
    STAGE_TWO_FEATURE_EXTRACTION,
    STAGE_THREE_DATA_PREPROCESSING,
    MODELS_DIR_SOL_ONE,
    MODELS_DIR_SOL_TWO,
    MODELS_DIR_SOL_THREE,
]:
    folder.mkdir(parents=True, exist_ok=True)

# Create Cleaning folder for each patient
JSON_PATIENTS_DETAILS = RAW_DATA_DIR / "patients_data_log.json"

df_data_log = pd.read_json(JSON_PATIENTS_DETAILS)
patient_ids = df_data_log["PatientID"].to_list()
for id in patient_ids:
    Path(STAGE_ONE_BASIC_CLEANING / id).mkdir(exist_ok=True)