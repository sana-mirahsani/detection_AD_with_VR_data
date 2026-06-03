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

## Phase-Level Features (mid_local)
### Phase 0: Tutorial vector (trajectory+event)

| Feature Type | CSV File | calculation method | Event typed to be used |
|------------|------------|------------|------------|
| phase_name | Both | extract from csv file name | - |
| phase_duration | events | extract from 'Duration_s' | Phase_End |
| reading_time_total,mean,median,std,max | events | extract from 'Activity_log' in all PANEL_DISMISSED| PANEL_DISMISSED|
| hover_count_total,hover_duration_total,mean,median,std,max | events | extract from 'Activity_log'| BUTTON_CLICKED,BUTTON_HOVER_START,HOVER_START|
| cv_hover_duration | events |std_hover_duration/mean_hover_duration (Coefficient of Variation) | - |
| hover_intensity |events|total_hover_duration/phase_duration | - |
| press_count_total,press_duration_total,mean,median,std,max | events | extract from 'Activity_log'| BUTTON_CLICKED,BUTTON_Pressed,BUTTON_SECTION_COMPLETE|
| press_intensity  | events |  std_press_duration / mean_press_duration  (Coefficient of Variation) | - |
| total_grab_count | events|count number of GRAB_START(not sure)  | - |
| total_grib_duration, mean, median, std, max  |events| extract from 'Activity_log' | Grab_realease |
| total_gaze_count  | events |  count number of GAZE_START(not sure)  |  |
| total_gaze_duration, mean, median, std, max  | events |  extract from 'Activity_log' | Gaze_realease |
| gaze_intensity  | events |  total_gaze_duration / phase_duration  | - |
| hover_vs_reading_time_ratio  | events |  total_hover_duration/total_reading_time  | - |
| hover_vs_active_interaction_ratio  | events |  total_hover_duration/total_press_duration  | - |
| interaction_fraction | events |(total_hover_duration+total_press_duration)/phase_duration|- |
|decision_latency | events | first_press_time - first_hover_time |-|
|clicks_per_second | events | total_press_count/phase_duration | - |
|hovers_per_click | events | total_hover_count/total_press_count| - |
|time_before_first_press | events | extract from PhaseTime_s| BUTTON_PRESSED or BUTTON_CLICKED |
|time_before_first_hover | events | extract from PhaseTime_s | BUTTON_HOVER_START |



## Global Feature Vector of all phases together (one paitent)
| Feature Type | calculation method |
Object recognition accuracy | 
Recognition response time (mean, per round)
Visuospatial placements correct
Socket rejection count
Memory recall accuracy
Mean recall latency
Mean placement error distance
