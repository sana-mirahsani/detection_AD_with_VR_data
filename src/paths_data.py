from pathlib import Path
import pandas as pd

# Root of the project
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Main Data folders
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
INTERIM_DATA_DIR = DATA_DIR / "interim"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
PREDICTIONS_DIR = DATA_DIR / "predictions"

# Sub Data Folder
STAGE_ONE_BASIC_CLEANING       = INTERIM_DATA_DIR / "stage_one_basic_cleaning"
STAGE_TWO_FEATURE_EXTRACTION   = INTERIM_DATA_DIR / "stage_two_feature_extraction"
STAGE_THREE_DATA_PREPROCESSING = INTERIM_DATA_DIR / "stage_three_data_preprocessing"

# Models
MODELS_DIR = PROJECT_ROOT / "models"

# Preprocessing
PREPROCESSING_DIR = PROJECT_ROOT / "preprocessing"

# Create directories if they don't exist
for folder in [
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
    PREDICTIONS_DIR,
    STAGE_ONE_BASIC_CLEANING,
    STAGE_TWO_FEATURE_EXTRACTION,
    STAGE_THREE_DATA_PREPROCESSING,
    MODELS_DIR,
    PREPROCESSING_DIR,
]:
    folder.mkdir(parents=True, exist_ok=True)

# Create Cleaning folder for each patient
JSON_PATIENTS_DETAILS = RAW_DATA_DIR / "patients_data_log.json"

df_data_log = pd.read_json(JSON_PATIENTS_DETAILS)
patient_ids = df_data_log["PatientID"].to_list()
for id in patient_ids:
    Path(STAGE_ONE_BASIC_CLEANING / id).mkdir(exist_ok=True)