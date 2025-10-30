| source | metadata_field | example_data | proposed_definition |
| --- | --- | --- | --- |
| csv, xlsx | Temps | 0301_SIM-brut.csv:Temps | temperature in Celsius |
| edf_header | TypeZone | kind=csv_header | type zone name |
| edf_header | vp:Voie(mm) | kind=csv_header | velocity (mm) |
| edf_header | vp:Cap(deg) | kind=csv_header | pressure (deg) |
| edf_header | vp:Pk(mm) | kind=csv_header | density (mm) |
| edf_header | vp:Vit(m/s) | kind=csv_header | specific volume (m/s) |
| edf_header | vp:Franchissement | kind=csv_header | flow rate (s) |
| edf_signal | TypeZone | label | type zone name |
| edf_signal | vp:Voie(mm) | transducer | velocity (mm) |
| edf_signal | vp:Cap(deg) | transducer | pressure (deg) |
| edf_signal | vp:Pk(mm) | transducer | density (mm) |
| edf_signal | vp:Vit(m/s) | transducer | specific volume (m/s) |
| edf_signal | vp:Franchissement | label | flow rate (s) |
