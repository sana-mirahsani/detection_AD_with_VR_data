import numpy as np
# empty dictionaries
patient_dict = {
    "Paitent_id"    : np.nan,
    "Age"           : np.nan,
    "Gender"        : np.nan,
    "dominant_hand" : np.nan,
    "Sessions_Completed_out_of_4" : np.nan, 
    "Help_Rating_out_of_5" : np.nan
}

# statistical features
reading_time_dict = {
    "reading_time_happened" : np.nan,
    "total_reading_time": np.nan,
    "mean_reading_time": np.nan,
    "max_reading_time": np.nan,
    "median_reading_time": np.nan,
    "std_reading_time": np.nan,
    "intensity_reading_time" : np.nan
}

hover_dict = {
    "hover_happened" : np.nan,
    "total_count_hover": np.nan,
    "total_duration_hover": np.nan,
    "mean_duration_hover": np.nan,
    "max_duration_hover": np.nan,
    "median_duration_hover": np.nan,
    "std_duration_hover": np.nan,
    "intensity_hover": np.nan
}

press_dict = {
    "press_happened" : np.nan,
    "total_count_press": np.nan,
    "total_duration_press": np.nan,
    "mean_duration_press": np.nan,
    "max_duration_press": np.nan,
    "median_duration_press": np.nan,
    "std_duration_press": np.nan,
    "intensity_press": np.nan # Interaction intensity
}

grab_dict = {
    "grab_happened" : np.nan,
    "total_count_grab": np.nan,
    "total_duration_grab": np.nan,
    "mean_duration_grab": np.nan,
    "max_duration_grab": np.nan,
    "median_duration_grab": np.nan,
    "std_duration_grab": np.nan,
    "intensity_grab": np.nan # Interaction intensity
}

gaze_dict = {
    "gaze_happened" : np.nan,
    "total_count_gaze": np.nan,
    "total_duration_gaze": np.nan,
    "mean_duration_gaze": np.nan,
    "max_duration_gaze": np.nan,
    "median_duration_gaze": np.nan,
    "std_duration_gaze": np.nan,
    "intensity_gaze": np.nan # Interaction intensity
}

# Behavioral features
behavior_dict = {
    "hover_vs_reading_time_ratio": np.nan,
    "hover_vs_active_interaction_ratio": np.nan,
    "interaction_fraction": np.nan,
    "decision_latency": np.nan,  
    "clicks_per_second": np.nan,
    "hovers_per_click": np.nan
}

# Temporal Features
temporal_dict = {
    "time_before_first_press": np.nan,
    "time_before_first_hover": np.nan
}

# Head features
headset_dict = {
    # Position features
    "head_total_distance": np.nan,

    "HMD_X_std": np.nan,
    "HMD_Y_std": np.nan,
    "HMD_Z_std": np.nan,

    "HMD_X_range": np.nan,
    "HMD_Y_range": np.nan,
    "HMD_Z_range": np.nan,

    # Speed features in ditance
    "mean_head_speed_in_distance": np.nan,
    "max_head_speed_in_distance": np.nan,
    "std_head_speed_in_distance": np.nan,

    # Orientation features
    "head_total_orientation" : np.nan,

    "Yaw_std": np.nan,
    "Pitch_std": np.nan,
    "Roll_std": np.nan,

    "Yaw_range": np.nan,
    "Pitch_range": np.nan,
    "Roll_range": np.nan,

    # Speed features in Orientation
    "mean_head_speed_in_orientation": np.nan,
    "max_head_speed_in_orientation": np.nan,
    "std_head_speed_in_orientation": np.nan,

    # Gaze features
    "gaze_obj_looked_ratio": np.nan,
    "gaze_switch_count": np.nan

}

# Hand features
controller_dict = {
    # Distance features
    "dominant_hand_total_distance": np.nan,
    "not_dominant_hand_total_distance": np.nan,

    # Speed features
    "dominant_hand_mean_speed": np.nan,
    "not_dominant_hand_mean_speed": np.nan,
    "dominant_hand_max_speed": np.nan,
    "not_dominant_hand_max_speed": np.nan,

    # Workspace_volume features
    "dominant_hand_x_range": np.nan,
    "dominant_hand_y_range": np.nan,
    "dominant_hand_z_range": np.nan,
    "not_dominant_hand_x_range": np.nan,
    "not_dominant_hand_y_range": np.nan,
    "not_dominant_hand_z_range": np.nan,

    # Press features
    "dominant_hand_trigger_press_count": np.nan,
    "not_dominant_hand_trigger_press_count": np.nan,
    "dominant_hand_trigger_pressure_mean": np.nan,
    "not_dominant_hand_trigger_pressure_mean": np.nan,

    # Grip count features
    "dominant_hand_grip_count": np.nan,
    "not_dominant_hand_grip_count": np.nan,
    "dominant_hand_grip_mean": np.nan,
    "not_dominant_hand_grip_mean": np.nan,
}

# extra features only for ObjectRecognition
obj_recognition_dict = {
                "ObjectRecognition_score": np.nan,
                "ObjectRecognition_mean_success_duration" : np.nan,
                "ObjectRecognition_mean_choose_wrong_obj": np.nan,
                "ObjectRecognition_total_duration": np.nan
            }

# extra features only for Visuospatial
visuospatial_dict = {
                "Visuospatial_score": np.nan,
                "Visuospatial_total_wrong_placement": np.nan,
                "Visuospatial_total_duration" : np.nan
                }

# extra features only for memory_dict
memory_dict = {
                "Memory_score": np.nan,
                "Memory_delay_first_action": np.nan,
                "Memory_total_wrong_recall" : np.nan,
                "Memory_mean_recall": np.nan,
                "Memory_cognitive_freez_count": np.nan,
                "Memory_cognitive_freez_mean_duration": np.nan,
                "Memory_total_duration" : np.nan
            }

phase_name_list = ['Tutorial', 'ObjectRecognition', 'Visuospatial', 'Memory']

clean_csv_file_correct_order = [
    '01_Tutorial_events.csv', '01_Tutorial_trajectory.csv',
    '02_ObjectRecognition_events.csv', '02_ObjectRecognition_trajectory.csv',
    '03_Visuospatial_events.csv', '03_Visuospatial_trajectory.csv',
    '04_Memory_events.csv', '04_Memory_trajectory.csv'
    ]