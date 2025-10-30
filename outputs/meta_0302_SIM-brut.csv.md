| source | metadata_field | example_data | proposed_definition |
| --- | --- | --- | --- |
| csv, xlsx | column_headers | Temps, TypeZone, vp:Voie(mm), vp:Cap(deg), vp:Pk(mm), vp:Vit(m/s), vp:Franchissement | Apnea-Hypopnea Index (events/hour) |
| edf_header | header-like_key | — | Apnea–Hypopnea Index (events/hour) |
| edf_signal | key=value tokens, units in parentheses | 0302_SIM-brut.csv: vp:Voie(mm), vp:Cap(deg), vp:Pk(mm), vp:Vit(m/s), vp:Franchissement | Apnea–Hypopnea Index (events/hour) |
| edf_signal | key=value tokens, units in parentheses | 0302_SIM-brut.csv: — | Apnea–Hypopnea Index (events/hour) |
| edf_signal | key=value patterns | 0302_SIM-brut.csv: vp:Voie(mm), vp:Cap(deg), vp:Pk(mm), vp:Vit(m/s), vp:Franchissement, — | Apnea-Hypopnea Index (events/hour) |
| edf_signal | units in parentheses | 0302_SIM-brut.csv: — | Apnea–Hypopnea Index (events/hour) |
| edf_signal | key=value patterns and lift keys as metadata fields | 0302_SIM-brut.csv: vp:Voie(mm), vp:Cap(deg), vp:Pk(mm), vp:Vit(m/s), vp:Franchissement, — | Apnea-Hypopnea Index (events/hour) |
| edf_signal | key=value patterns and lift keys as metadata fields | 0302_SIM-brut.csv: —, —, —, —, — | Apnea–Hypopnea Index (events/hour) |
| edf_signal | units in parentheses and key=value patterns | 0302_SIM-brut.csv: vp:Voie(mm), vp:Cap(deg), vp:Pk(mm), vp:Vit(m/s), vp:Franchissement, — | Apnea-Hypopnea Index (events/hour) |
| edf_signal | units in parentheses and key=value patterns | 0302_SIM-brut.csv: —, —, —, —, — | Apnea–Hypopnea Index (events/hour) |
| edf_signal | key=value patterns with lift keys as metadata fields | 0302_SIM-brut.csv: vp:Voie(mm), vp:Cap(deg), vp:Pk(mm), vp:Vit(m/s), vp:Franchissement, — | Apnea-Hypopnea Index (events/hour) |
| edf_signal | key=value patterns with lift keys as metadata fields | 0302_SIM-brut.csv: —, —, —, —, — | Apnea–Hypopnea Index (events/hour) |
| edf_signal | units in parentheses and key=value patterns with lift keys as metadata fields | 0302_SIM-brut.csv: vp:Voie(mm), vp:Cap(deg), vp:Pk(mm), vp:Vit(m/s), vp:Franchissement, — | Apnea-Hypopnea Index (events/hour) |
| edf_signal | units in parentheses and key=value patterns with lift keys as metadata fields | 0302_SIM-brut.csv: —, —, —, —, — | Apnea–Hypopnea Index (events/hour) |
| edf_signal | key=value patterns with lift keys as metadata fields | 0302_SIM-brut.csv: vp:Voie(mm), vp:Cap(deg), vp:Pk(mm), vp:Vit(m/s), vp:Franchissement, — | Apnea-Hypopnea Index (events/hour) |
| edf_signal | key=value patterns with lift keys as metadata fields | 0302_SIM-brut.csv: —, —, —, —, — | Apnea–Hypopnea Index (events/hour) |
Note: The example_data is provided in the first row of each EDF signal.
