import fastf1
import matplotlib.pyplot as plt
import sys
from datetime import datetime
import pandas as pd
import matplotlib.dates
from scipy import stats
import numpy as np
import csv
import os

fastf1.Cache.enable_cache('cache/')  


tyreAvailability = {"SOFT": 8, "MEDIUM": 3, "HARD": 2}
driver = "16"

fuelCapacity = 110
num_laps = 70

fuel_per_lap = fuelCapacity/num_laps
laptime_per_kg_of_fuel = 0.03 * 1000 # milliseconds
laptime_gained_per_lap = laptime_per_kg_of_fuel * fuel_per_lap


session_name = "race"
session = fastf1.get_session(2022, 'hungary', session_name)
session.load()

session_data = session.laps[["DriverNumber", "LapTime", "LapNumber", "PitOutTime", "PitInTime", "Compound", "TyreLife", "Stint", "IsAccurate"]]
Compounds = session_data[session_data["DriverNumber"]==driver]["Compound"].copy().to_list()
TyreLife = session_data[session_data["DriverNumber"]==driver]["TyreLife"].copy().to_list()

PitOutTime = session_data[session_data["DriverNumber"]==driver]["PitOutTime"].copy().to_numpy()
print(Compounds)
print(TyreLife)

IsPitStop = [(np.isnat(x) == False) for x in PitOutTime]
print(IsPitStop)

PitStopLaps = []
for i in range(70):
    if IsPitStop[i]:
        PitStopLaps.append(i+1)

if PitStopLaps[0] == 1:
    PitStopLaps.pop(0)

ActualTyreSchedule = []
CurrentTyre = "DUMMY"
for count,val in enumerate(Compounds):
    if IsPitStop[count]:
        tyreLifeCount = 0
        if TyreLife[count] != 1:
            tyreLifeCount = int(TyreLife[count])
        CurrentTyre = Compounds[count] + " " + str(tyreLifeCount)
    ActualTyreSchedule.append(CurrentTyre)

csvFileName = 'DATA/DRIVER' + driver + '/RealTyreSchedule.csv'
if os.path.exists(csvFileName):
    os.remove(csvFileName)
with open(csvFileName, 'w', newline='') as myfile:
     wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
     wr.writerow(ActualTyreSchedule)

csvFileName = 'DATA/DRIVER' + driver + '/RealPitStopSchedule.csv'
if os.path.exists(csvFileName):
    os.remove(csvFileName)
with open(csvFileName, 'w', newline='') as myfile:
     wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
     wr.writerow(PitStopLaps)

# tyreAvailability = {"SOFT": 8, "MEDIUM": 3, "HARD": 2}
# driver = "4"

# fuelCapacity = 110
# num_laps = 70

# def convert(td):
#     print(td.components)
#     time = td.components.minutes*60 + td.components.seconds
#     time = time * 1000 + td.components.milliseconds
#     return time

# def get_tyres_used(session_name):
#     session = fastf1.get_session(2022, 'hungary', session_name)
#     session.load()
    
#     session_data = session.laps[["DriverNumber", "LapTime", "LapNumber", "PitOutTime", "PitInTime", "Compound", "TyreLife", "Stint", "IsAccurate"]]

#     tyre_types = {"SOFT":[], "MEDIUM":[], "HARD": []}
#     stints = {}
#     prev_life = 0
#     prev_type = ""
#     current_stint = 1
#     appendTo = 1
#     seq = []
#     driver_index = 0
#     initTyreLife = 1
#     for index, lap in session_data.iterlaps():
#         if lap["Compound"] not in tyre_types:
#             continue    
#         if lap["DriverNumber"] == driver:
#             print(lap["LapTime"], " ", lap["LapNumber"], " ", lap["Compound"], " ", lap["TyreLife"], " ", lap["Stint"])
#             tyreLife = int(lap["TyreLife"])
        
            
#             if (tyreLife <= prev_life or prev_type != lap["Compound"]) and driver_index>0 : # tyre change occurred change stint
                
#                 if initTyreLife == 1:
#                     appendTo = current_stint
                    
#                 else:
#                     for stint in tyre_types[prev_type]:
#                         if stints[stint][-1] == initTyreLife - 1:
#                             appendTo = stint

#                 if appendTo not in stints:
#                     stints[appendTo] = seq
#                     tyre_types[prev_type].append(current_stint) 
#                 else: 
#                     stints[appendTo].extend(seq)

                
#                 seq = []
#                 initTyreLife = tyreLife                
#                 current_stint+=1
#             seq.append(tyreLife)  

#             prev_life = tyreLife
#             prev_type = lap["Compound"]
#             driver_index+=1


#     if prev_type in tyre_types:
#         if initTyreLife == 1:
#             appendTo = current_stint
            
#         else:
#             for stint in tyre_types[prev_type]:
#                 if stints[stint][-1] == initTyreLife - 1:
#                     appendTo = stint

#         if appendTo not in stints:
#             stints[appendTo] = seq
#             tyre_types[prev_type].append(current_stint) 
#         else: 
#             stints[appendTo].extend(seq)
    
#     return tyre_types, stints, session_data

# def aggregate_tyres(stints, stint_types):
#     new_stints = {}
#     for stint in stints:
#         slope, intercept, r, p, std_err = stats.linregress(stints[stint][0], stints[stint][1])
#         def myfunc(x):
#             return slope * x + intercept

#         indices = [i for i in range(0, 2*num_laps)]
#         reg_results = list(map(myfunc, indices))
#         new_stints[stint] = [indices, reg_results]

#     final_stint_types = {}
#     for stint_type in stint_types:
#         all = []
#         for stint in stint_types[stint_type]:
#             all.append(new_stints[stint][1])
#         all = np.mean(np.array(all), axis = 0)
#         final_stint_types[stint_type] = [indices, all]

#     return final_stint_types
    


# fastf1.Cache.enable_cache('cache/')  


# fuel_per_lap = fuelCapacity/num_laps
# laptime_per_kg_of_fuel = 0.03 * 1000 # milliseconds
# laptime_gained_per_lap = laptime_per_kg_of_fuel * fuel_per_lap


# tyre_types_fp1 , stints_fp1, session_data = get_tyres_used("race")
# print(tyre_types_fp1)
# print(stints_fp1)
# print(session_data)

# ActualTyreSchedule = ["dummy" for x in range(70)]

# for key1,val1 in tyre_types_fp1.items():
#     for key2,val2 in stints_fp1.items():
#         for val3 in val2:
#             ActualTyreSchedule[val3 - 1] = key1
# print(ActualTyreSchedule)