| source | metadata_field | example_data | proposed_definition |
| --- | --- | --- | --- |
| csv/xlsx | Temps | 0302_SIM-brut.csv | temperature in Celsius, time of day |
| edf_header | TypeZone | vp:Voie(mm), vp:Cap(deg), vp:Pk(mm), vp:Vit(m/s) | type zone name |
| edf_signal | vp:Voie(mm) | 0302_SIM-brut.csv | temperature in Celsius, time of day |
| edf_signal | vp:Cap(deg) | 0302_SIM-brut.csv | temperature in degrees Celsius, time of day |
| edf_signal | vp:Pk(mm) | 0302_SIM-brut.csv | temperature in millimeters, time of day |
| edf_signal | vp:Vit(m/s) | 0302_SIM-brut.csv | temperature in centimeters per second, time of day |
| edf_signal | vp:Franchissement | 0302_SIM-brut.csv | temperature in degrees Celsius, fractional change in the temperature scale, time of day |
| csv/xlsx | commentaires | file=0302_SIM-brut.csv | comments or notes about the data |
| csv/xlsx | n_records | — | number of records |
| csv/xlsx | record_duration_s | 1.5 | duration of one minute in seconds |
| edf_header | patient_id | — | unique identifier for each patient |
| edf_signal | startdate | — | date when the data was collected, e.g., 2023-04-01 |
| edf_signal | starttime | — | time at which the first measurement occurred, e.g., 9:00 AM |
| edf_signal | header_bytes | — | bytes of metadata in the EDF file, not used for this example |
| edf_signal | n_signals | 2 | number of signals collected |
| csv/xlsx | phys_dim | — | physical dimensions of the data (e.g., mm, cm) |
| csv/xlsx | fs_hz | 1000000 | sampling frequency in Hz for EDF files |
This table provides a metadata dictionary based on the given context.
