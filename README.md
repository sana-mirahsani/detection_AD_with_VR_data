# detection_AD_with_VR_data

## possible feature extraction of each event (local=in one section)

| Event Type | Possible feature extraction (directly) | Possible feature extraction (needs calculation) | 
|------------|------------|
| PHASE_START/PHASE_END | Nothing, it works in global  | -
| SECTION_START/SECTION_END |  section_duration  | -
| PANEL_SHOWN/PANEL_DISMISSED | reading time | -
| BUTTON_HOVER_START/_END |  |  hover_count_total, hover_duration_total, mean, median, max, 


## possible feature extraction of each event (global=in one phase)

| Event Type | Possible feature extraction | 
|------------|------------|
| PHASE_START / PHASE_END |      | 
| SECTION_START/SECTION_END  |  Nothing,it works in local  | 

## Feature vector of toturial_event.csv 
| Feature Type | calculation method | Event typed to be used |
|------------|------------|------------|
| section_duration | extract from 'Duration' in SECTION_END | SECTION_END |
| reading_time  |  extract from 'Activity_log' in PANEL_DISMISSED  | PANEL_DISMISSED |
| total_hover_count  |  extract from 'Activity_log'  | BUTTON_CLICKED, BUTTON_HOVER_START |
| total_hover_duration  |  extract from 'Activity_log' in PANEL_DISMISSED  | PANEL_DISMISSED |
| reading_time  |  extract from 'Activity_log' in PANEL_DISMISSED  | PANEL_DISMISSED |
