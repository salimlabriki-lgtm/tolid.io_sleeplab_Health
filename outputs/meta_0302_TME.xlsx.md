| source | metadata_field | example_data | proposed_definition |
| --- | --- | --- | --- |
| csv,xlsx | Heure de début | 07:30,19:45 | Apnea-Hypopnea Index (events/hour) |
| csv,xlsx | Heure de fin | 20:30,22:45 | Apnea-Hypopnea Index (events/hour) |
| edf_header | Événement | TME, SIM | Start Time |
| edf_signal | Durée | TME, SIM | Début du temps métrique |
| csv,xlsx | Événement | 07:30,19:45 | Apnea-Hypopnea Index (events/hour) |
| csv,xlsx | Événement | 20:30,22:45 | Apnea-Hypopnea Index (events/hour) |
| edf_header | Durée | TME, SIM | Début du temps métrique |
| edf_signal | Heure de début | 07:30,19:45 | Start Time |
| edf_signal | Heure de fin | 20:30,22:45 | End Time |
Note that the proposed definition for "Start Time" is conservative and based on a consistent column pattern.
