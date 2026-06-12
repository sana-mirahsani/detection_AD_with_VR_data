# empty dictionaries
patient_dict = {
    "Paitent_id"    : None,
    "Age"           : None,
    "Gender"        : None,
    "dominant_hand" : None,
    "Sessions_Completed_out_of_4" : None, 
    "Help_Rating_out_of_5" : None
}

# statistical features
reading_time_dict = {
    "total_reading_time": None,
    "mean_reading_time": None,
    "max_reading_time": None,
    "median_reading_time": None,
    "std_reading_time": None,
    "intensity_reading_time" : None
}

hover_dict = {
    "total_count_hover": None,
    "total_duration_hover": None,
    "mean_duration_hover": None,
    "max_duration_hover": None,
    "median_duration_hover": None,
    "std_duration_hover": None,
    "intensity_hover": None
}

press_dict = {
    "total_count_press": None,
    "total_duration_press": None,
    "mean_duration_press": None,
    "max_duration_press": None,
    "median_duration_press": None,
    "std_duration_press": None,
    "intensity_press": None # Interaction intensity
}

grab_dict = {
    "total_count_grab": None,
    "total_duration_grab": None,
    "mean_duration_grab": None,
    "max_duration_grab": None,
    "median_duration_grab": None,
    "std_duration_grab": None,
    "intensity_grab": None # Interaction intensity
}

gaze_dict = {
    "total_count_gaze": None,
    "total_duration_gaze": None,
    "mean_duration_gaze": None,
    "max_duration_gaze": None,
    "median_duration_gaze": None,
    "std_duration_gaze": None,
    "intensity_gaze": None # Interaction intensity
}

# Behavioral features
behavior_dict = {
    "hover_vs_reading_time_ratio": None,
    "hover_vs_active_interaction_ratio": None,
    "interaction_fraction": None,
    "decision_latency": None,  
    "clicks_per_second": None,
    "hovers_per_click": None
}

# Temporal Features
temporal_dict = {
    "time_before_first_press": None,
    "time_before_first_hover": None
}

# Head features
headset_dict = {
    # Position features
    "head_total_distance": None,

    "HMD_X_std": None,
    "HMD_Y_std": None,
    "HMD_Z_std": None,

    "HMD_X_range": None,
    "HMD_Y_range": None,
    "HMD_Z_range": None,

    # Speed features in ditance
    "mean_head_speed_in_distance": None,
    "max_head_speed_in_distance": None,
    "std_head_speed_in_distance": None,

    # Orientation features
    "head_total_orientation" : None,

    "Yaw_std": None,
    "Pitch_std": None,
    "Roll_std": None,

    "Yaw_range": None,
    "Pitch_range": None,
    "Roll_range": None,

    # Speed features in Orientation
    "mean_head_speed_in_orientation": None,
    "max_head_speed_in_orientation": None,
    "std_head_speed_in_orientation": None,

    # Gaze features
    "gaze_obj_looked_ratio": None,
    "gaze_switch_count": None

}

# Hand features
controller_dict = {
    # Distance features
    "dominant_hand_total_distance": None,
    "not_dominant_hand_total_distance": None,

    # Speed features
    "dominant_hand_mean_speed": None,
    "not_dominant_hand_mean_speed": None,
    "dominant_hand_max_speed": None,
    "not_dominant_hand_max_speed": None,

    # Workspace_volume features
    "dominant_hand_x_range": None,
    "dominant_hand_y_range": None,
    "dominant_hand_z_range": None,
    "not_dominant_hand_x_range": None,
    "not_dominant_hand_y_range": None,
    "not_dominant_hand_z_range": None,

    # Press features
    "dominant_hand_trigger_press_count": None,
    "not_dominant_hand_trigger_press_count": None,
    "dominant_hand_trigger_pressure_mean": None,
    "not_dominant_hand_trigger_pressure_mean": None,

    # Grip count features
    "dominant_hand_grip_count": None,
    "not_dominant_hand_grip_count": None,
    "dominant_hand_grip_mean": None,
    "not_dominant_hand_grip_mean": None,
}

# extra features only for ObjectRecognition
obj_recognition_dict = {
                "obj_recognition_score": None,
                "obj_recognition_mean_success_duration" : None,
                "obj_recognition_mean_choose_wrong_obj": None,
                "obj_recognition_total_duration": None
            }

# extra features only for Visuospatial
visuospatial_dict = {
                "visuospatial_score": None,
                "visuospatial_total_wrong_placement": None,
                "visuospatial_total_duration" : None
                }

# extra features only for memory_dict
memory_dict = {
                "memory_score": None,
                "memory_delay_first_action": None,
                "memory_total_wrong_recall" : None,
                "memory_mean_recall": None,
                "memory_cognitive_freez_count": None,
                "memory_cognitive_freez_mean_duration": None,
                "memory_total_duration" : None
            }

phase_name_list = ['Tutorial', 'ObjectRecognition', 'Visuospatial', 'Memory']