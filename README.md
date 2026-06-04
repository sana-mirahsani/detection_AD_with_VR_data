# detection_AD_with_VR_data

## Section-Level Features (local) == Not used for now due to the high numbers of columns
| Feature Type | calculation method | Event typed to be used |
|------------|------------|------------|
| section_id | a counter function | - |
| section_name | extract from "section" column | - |
| section_duration | extract from 'Duration' in SECTION_END | SECTION_END |
| reading_time  |  extract from 'Activity_log' in PANEL_DISMISSED  | PANEL_DISMISSED |
| total_hover_count  |  extract from 'Activity_log'  | BUTTON_CLICKED, BUTTON_HOVER_START;HOVER_STARTHOVER_END |
| total_hover_duration, mean, median, std, max  |  extract from 'Activity_log' | BUTTON_CLICKED, BUTTON_HOVER_START,HOVER_START |
| cv_hover_duration  |  std_hover_duration/mean_hover_duration  (Coefficient of Variation) | - |
| hover_intensity  |  total_hover_duration/section_total_time  | - |
| total_press_count |  extract from 'Activity_log'  | BUTTON_CLICKED, BUTTON_Pressed;BUTTON_SECTION_COMPLETE |
| total_press_duration,mean,median,std,max|extract from 'Activity_log' | BUTTON_CLICKED, BUTTON_Pressed|
| press_intensity  |  std_press_duration / mean_press_duration  (Coefficient of Variation) | - |
| total_grab_count  |  count number of GRAB_START(not sure)  | - |
| total_grib_duration, mean, median, std, max  |  extract from 'Activity_log' | Grab_realease |
| grab_intensity  |  total_grab_duration / section_total_time  | - |
| total_gaze_count  |  count number of GAZE_START(not sure)  |  |
| total_gaze_duration, mean, median, std, max  |  extract from 'Activity_log' | Gaze_realease |
| gaze_intensity  |  total_gaze_duration / section_total_time  | - |
| hover_vs_reading_time_ratio  |  total_hover_duration/total_reading_time  | - |
| hover_vs_active_interaction_ratio  |  total_hover_duration/total_press_duration  | - |
| interaction_fraction |(total_hover_duration+total_press_duration)/section_duration|- |
|decision_latency | first_press_time - first_hover_time |-|
|clicks_per_second | total_press_count/section_duration | - |
|hovers_per_click | total_hover_count/total_press_count| - |
|time_before_first_press | extract from PhaseTime_s| BUTTON_PRESSED or BUTTON_CLICKED |
|time_before_first_hover | extract from PhaseTime_s | BUTTON_HOVER_START |

## Phase-Level Features for all phases (mid_local)
### Event vector
| Feature Type | CSV File | calculation method | Event typed to be used |
|------------|------------|------------|------------|
| phase_name | events | extract from csv file name | - |
| phase_duration | events | extract from 'Duration_s' | Phase_End |
| reading_time_total,mean,median,std,max | events | extract from 'Activity_log' in all PANEL_DISMISSED| PANEL_DISMISSED|
| reading_time_intensity |events|total_reading_time_duration/phase_duration | - |
| hover_count_total,hover_duration_total,mean,median,std,max | events | extract from 'Activity_log'| BUTTON_CLICKED,BUTTON_HOVER_START,HOVER_START|
| cv_hover_duration | events |std_hover_duration/mean_hover_duration (Coefficient of Variation) | - |
| hover_intensity |events|total_hover_duration/phase_duration | - |
| press_count_total,press_duration_total,mean,median,std,max | events | extract from 'Activity_log'| BUTTON_CLICKED,BUTTON_Pressed,BUTTON_SECTION_COMPLETE|
| press_intensity | events |total_press_duration/phase_duration| - |
| total_grab_count | events|count number of GRAB_START(not sure)  | - |
| total_grib_duration, mean, median, std, max  |events| extract from 'Activity_log' | Grab_realease |
| grab_intensity | events |total_grab_duration/phase_duration| - |
| total_gaze_count | events |  count number of GAZE_START(not sure)  |  |
| total_gaze_duration, mean, median, std, max  | events |  extract from 'Activity_log' | Gaze_realease |
| gaze_intensity | events |  total_gaze_duration / phase_duration  | - |
| hover_vs_reading_time_ratio | events | total_hover_duration/total_reading_time | - |
| hover_vs_active_interaction_ratio | events | total_hover_duration/total_press_duration | - |
| interaction_fraction | events |(total_hover_duration+total_press_duration)/phase_duration|- |
|decision_latency | events | first_press_time - first_hover_time |-|
|clicks_per_second | events | total_press_count/phase_duration | - |
|hovers_per_click | events | total_hover_count/total_press_count| - |
|time_before_first_press | events | extract from PhaseTime_s| BUTTON_PRESSED or BUTTON_CLICKED |
|time_before_first_hover | events | extract from PhaseTime_s| BUTTON_HOVER or HOVER_START |

### Trajectory vector
| Feature Type | calculation method | What information does it give |
|------------|------------|------------|
|head_total_distance|distance += sqrt((dx)**2 + (dy)**2 + (dz)**2)|Position|
|HMD_X_std|calculate from HMD_X column| Position|
|HMD_Y_std|calculate from HMD_Y column |Position|  
|HMD_Z_std|calculate from HMD_Z column |Position|  
|HMD_X_range|max(X)-min(X)|Position|  
|HMD_Y_range|max(Y)-min(Y)|Position|  
|HMD_Z_range|max(Z)-min(Z)|Position|
|mean_head_speed|dt = t[i] - t[i-1], t = PhaseTime_s, speed = distance / dt|Speed|  
|max_head_speed|dt = t[i] - t[i-1], t = PhaseTime_s, speed = distance / dt|Speed|  
|std_head_speed|dt = t[i] - t[i-1], t = PhaseTime_s, speed = distance / dt|Speed| 
|Yaw_std|calculate from HMD_Yaw column|Orientation|
|Pitch_std|calculate from HMD_Pitch column|Orientation|
|Roll_std|calculate from HMD_Roll column|Orientation|
|Yaw_range|calculate from HMD_Yaw column|Orientation|
|Pitch_range|calculate from HMD_Pitch column|Orientation|
|Roll_range|calculate from HMD_Roll column|Orientation|
|exploration_index| Yaw_range + Pitch_range |Exploration |
|dominant_hand_total_distance|distance += sqrt((dx)**2 + (dy)**2 + (dz)**2)|Distance|
|not_dominant_hand_total_distance|distance += sqrt((dx)**2 + (dy)**2 + (dz)**2)|Distance|
|dominant_hand_mean_speed|with phasetime_s column| hand speed|
|not_dominant_hand_mean_speed|with phasetime_s column|hand speed|
|dominant_hand_max_speed|with phasetime_s column|hand speed|
|not_dominant_hand_max_speed|with phasetime_s column|hand speed|
|dominant_hand_x_range|(right)LeftCtrl_X|workspace_volume|
|dominant_hand_y_range|(right)LeftCtrl_Y|workspace_volume|
|dominant_hand_z_range|(right)LeftCtrl_Z|workspace_volume|
|not_dominant_hand_x_range|(right)LeftCtrl_X|workspace_volume|
|not_dominant_hand_y_range|(right)LeftCtrl_Y|workspace_volume|
|not_dominant_hand_z_range|(right)LeftCtrl_Z|workspace_volume|
|dominant_hand_trigger_active_time||Active time|
|not_dominant_hand_trigger_active_time||Active time|
|dominant_hand_trigger_press_count||Press count|
|not_dominant_hand_trigger_press_count||Press count|
|dominant_hand_grab_count||Grab|
|not_dominant_hand_grab_count||Grab|
|dominant_hand_mean_grap_duration||Grab|
|not_dominant_hand_mean_grap_duration||Grab|
|hand_movement_symmetry|||
|gaze_target_counts|فراوانی نگاه به هر هدف||
|gaze_switch_count||

Number of column (for one phase) after feature extraction for both trajectory + events file =~ 60

Number of column (for all 4 phases) =~ 4 * 60

## (Global) Paitent-Level Feature Vector of all phases together (one paitent)
| Feature Type | calculation method | What does it mean | Phase_name |
|------------|------------|------------|------------|
|Object_recognition_accuracy|ROUND_RESULT/SCORING_SUMMARY| Direct measure of object recognition|ObjectRecognition_events|
|Recognition_response_time (mean, per round)|SELECTION_CORRECT Duration_s|Processing speed; slowing is an early signal|Object Recognition|
|Visuospatial_placements_correct|VISUOSPATIAL_COMPLETE|Spatial mapping ability|Visuospatial|
|Socket_rejection_count|SOCKET_REJECTION|Spatial errors and uncertainty|Visuospatial|
|Memory_recall_accuracy|MEMORY_RECALL / SCORING_SUMMARY|Delayed recall — central to the assessment|Memory|
|Mean_recall_latency|MEMORY_RECALL RecallTime|Spatial errors and uncertainty|Memory|
|Mean_placement_error_distance|MEMORY_RECALL ErrorDistance|Severity of spatial-memory error, not just right/wrong| Memory|
|Carry time per object|OBJECT_CARRY_TIME CarryTime|Long carries suggest indecision about placement|Visuospatial|
|Pickup count per object|OBJECT_CARRY_TIME PickupCount|Repeated pickups indicate uncertainty|Visuospatial|
|Cognitive freeze count/duration|COGNITIVE_FREEZE|Mid-task processing pauses|Visuospatial,Memory|
|Re-grab delay after rejection|POST_REJECTION_GAZE DelayToReGrab|Time to recover from a placement error|Visuospatial|
|Gazed-correct-socket-after-rejection|POST_REJECTION_GAZE GazedCorrectSocket|Whether the patient can locate the right answer after failing|Visuospatial|
|Hover count before grab|HOVER_START count per object|Many hovers can signal indecision|Visuospatial,Memory,Tutorial|
|Recall first-action delay|	RECALL_FIRST_ACTION DelayFromPhaseStart|Time to begin retrieving — planning latency|Memory|
|Hand path length|Sum of frame-to-frame controller displacement	|Inefficient, wandering reaches|all phases|
|Hand speed (mean, peak)|Displacement ÷ time between samples|Bradykinesia / slowed movement|all phases|
|Hand jitter|Standard deviation of speed change (jerk)|Tremor and reduced motor smoothness proxy|all phases|
|Head path length|Sum of frame-to-frame HMD displacement|Restlessness or excess head motion|all phases|
|Yaw reversals / total yaw|Sign changes in head-yaw difference|Scanning behaviour; disorganised search|all phases|
|Gaze-on-target percentage|Fraction of samples with GazeTarget ≠ None|Sustained attention to task-relevant objects|all phases|
|Gaze switch count|Number of GazeTarget changes|Attention shifting / distractibility|all phases|

23 columns for one paitent.

## Final vector feature
Paitent_id, Age, Gender, Sessions_Completed_out_of_4, Help_Rating_out_of_5, 
Phase-Level Features (Trajectory+Event), Paitent-Level feature

total columns for one paitent : 288


