| source | metadata_field | example_data | proposed_definition |
| --- | --- | --- | --- |
| csv | Heure de début,Heure de fin,Événement,Durée,Volume audio dB (moy),Voltage_Voltage_Vigisim (moy) | 2019-03-01T08:00:00,2019-04-01T16:00:00,Evénement 1,Durée 5 min,Volume audio 70 dB,Voltage_Voltage_Vigisim 1.2 | Heure de début and Fin du répertoire sont des champs que nous ne devons pas inclure car ils n'ont aucune valeur.
| csv | Événement,Heure de début,Heure de fin,Durée,Volume audio dB (moy),Voltage_Voltage_Vigisim (moy) | 1,2019-03-01T08:00:00,2019-04-01T16:00:00,Evénement 1,Durée 5 min,Volume audio 70 dB,Voltage_Voltage_Vigisim 1.2 | Étant donné que nous ne devons pas inclure les Heures de début et Fin du répertoire dans le DataFrame, on peut supprimer ces colonnes.
| csv | Evénement,Durée,Volume audio dB (moy),Voltage_Voltage_Vigisim (moy) | 1,Evénement 1,Durée 5 min,Volume audio 70 dB,Voltage_Voltage_Vigisim 1.2 | 
| edf_header | Heure de début,Heure de fin,Événement,Durée,Volume audio dB (moy),Voltage_Voltage_Vigisim (moy) | 2019-03-01T08:00:00,2019-04-01T16:00:00,Evénement 1,Durée 5 min,Volume audio 70 dB,Voltage_Voltage_Vigisim 1.2 | 
| edf_signal | Evénement,Heure de début,Heure de fin,Durée,Volume audio dB (moy),Voltage_Voltage_Vigisim (moy) | 1,Evénement 1,2019-03-01T08:00:00,2019-04-01T16:00:00,Durée 5 min,Volume audio 70 dB,Voltage_Voltage_Vigisim 1.2 |
