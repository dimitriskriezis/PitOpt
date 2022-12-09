import fastf1
import matplotlib.pyplot as plt
import sys
from datetime import datetime
import pandas as pd
import matplotlib.dates
from scipy import stats
import numpy as np

tyreAvailability = {"SOFT": 8, "MEDIUM": 3, "HARD": 2}
driver = "16"

fuelCapacity = 110
num_laps = 70

def convert(td):
    print(td.components)
    time = td.components.minutes*60 + td.components.seconds
    time = time * 1000 + td.components.milliseconds
    return time

def get_tyres_used(session_name):
    session = fastf1.get_session(2022, 'hungary', session_name)
    session.load()
    
    session_data = session.laps[["DriverNumber", "LapTime", "LapNumber", "PitOutTime", "PitInTime", "Compound", "TyreLife", "Stint", "IsAccurate"]]

    tyre_types = {"SOFT":[], "MEDIUM":[], "HARD": []}
    stints = {}
    prev_life = 0
    prev_type = ""
    current_stint = 1
    appendTo = 1
    seq = []
    driver_index = 0
    initTyreLife = 1
    for index, lap in session_data.iterlaps():
        if lap["Compound"] not in tyre_types:
            continue    
        if lap["DriverNumber"] == driver:
            print(lap["LapTime"], " ", lap["LapNumber"], " ", lap["Compound"], " ", lap["TyreLife"], " ", lap["Stint"])
            tyreLife = int(lap["TyreLife"])
        
            
            if (tyreLife <= prev_life or prev_type != lap["Compound"]) and driver_index>0 : # tyre change occurred change stint
                
                if initTyreLife == 1:
                    appendTo = current_stint
                    
                else:
                    for stint in tyre_types[prev_type]:
                        if stints[stint][-1] == initTyreLife - 1:
                            appendTo = stint

                if appendTo not in stints:
                    stints[appendTo] = seq
                    tyre_types[prev_type].append(current_stint) 
                else: 
                    stints[appendTo].extend(seq)

                
                seq = []
                initTyreLife = tyreLife                
                current_stint+=1
            seq.append(tyreLife)  

            prev_life = tyreLife
            prev_type = lap["Compound"]
            driver_index+=1


    if prev_type in tyre_types:
        if initTyreLife == 1:
            appendTo = current_stint
            
        else:
            for stint in tyre_types[prev_type]:
                if stints[stint][-1] == initTyreLife - 1:
                    appendTo = stint

        if appendTo not in stints:
            stints[appendTo] = seq
            tyre_types[prev_type].append(current_stint) 
        else: 
            stints[appendTo].extend(seq)
    
    return tyre_types, stints

def aggregate_tyres(stints, stint_types):
    new_stints = {}
    for stint in stints:
        slope, intercept, r, p, std_err = stats.linregress(stints[stint][0], stints[stint][1])
        def myfunc(x):
            return slope * x + intercept

        indices = [i for i in range(0, 2*num_laps)]
        reg_results = list(map(myfunc, indices))
        new_stints[stint] = [indices, reg_results]

    final_stint_types = {}
    for stint_type in stint_types:
        all = []
        for stint in stint_types[stint_type]:
            all.append(new_stints[stint][1])
        all = np.mean(np.array(all), axis = 0)
        final_stint_types[stint_type] = [indices, all]

    return final_stint_types
    


fastf1.Cache.enable_cache('cache/')  


fuel_per_lap = fuelCapacity/num_laps
laptime_per_kg_of_fuel = 0.03 * 1000 # milliseconds
laptime_gained_per_lap = laptime_per_kg_of_fuel * fuel_per_lap


# session_fp1 = fastf1.get_session(2022, 'hungary', 'practice 1')
# session_fp1.load()
# print(session_fp1)
# session_fp1_data = session_fp1.laps[["DriverNumber", "LapTime", "LapNumber", "PitOutTime", "PitInTime", "Compound", "TyreLife", "Stint", "IsAccurate"]]

# for index, lap in session_fp1_data.iterlaps():
#     if lap["DriverNumber"] == driver:
#         print(lap["LapTime"], " ", lap["LapNumber"], " ", lap["Compound"], " ", lap["TyreLife"], " ", lap["Stint"])
# print()
# print("fp2")
# print()

# session_fp2 = fastf1.get_session(2022, 'hungary', 'practice 2')
# session_fp2.load()
# session_fp2_data = session_fp2.laps[["DriverNumber", "LapTime", "LapNumber", "PitOutTime", "PitInTime", "Compound", "TyreLife", "Stint", "IsAccurate"]]

# for index, lap in session_fp2_data.iterlaps():
#     if lap["DriverNumber"] == driver:
#         print(lap["LapTime"], " ", lap["LapNumber"], " ", lap["Compound"], " ", lap["TyreLife"], " ", lap["Stint"])
# print()
# print("FP3")
# print()


# session_fp2 = fastf1.get_session(2022, 'hungary', 'practice 3')
# session_fp2.load()
# session_fp2_data = session_fp2.laps[["DriverNumber", "LapTime", "LapNumber", "PitOutTime", "PitInTime", "Compound", "TyreLife", "Stint", "IsAccurate"]]

# for index, lap in session_fp2_data.iterlaps():
#     if lap["DriverNumber"] == driver:
#         print(lap["LapTime"], " ", lap["LapNumber"], " ", lap["Compound"], " ", lap["TyreLife"], " ", lap["Stint"])
# print()
# print("QUALIFYING")
# print()

# session_quali = fastf1.get_session(2022, 'hungary', 'q')
# session_quali.load()
# session_quali_data = session_quali.laps[["DriverNumber", "LapTime", "LapNumber", "PitOutTime", "PitInTime", "Compound", "TyreLife", "Stint", "IsAccurate"]]

# for index, lap in session_quali_data.iterlaps():
#     if lap["DriverNumber"] == driver:
#         print(lap["LapTime"], " ", lap["LapNumber"], " ", lap["Compound"], " ", lap["TyreLife"], " ", lap["Stint"])

######################## ANALYZING RACE DATA ########################
#####################################################################
tyre_types_fp1 , stints_fp1 = get_tyres_used("practice 1")
print(tyre_types_fp1)
print(stints_fp1)
tyre_types_fp2 , stints_fp2 = get_tyres_used("practice 2")
print(tyre_types_fp2)
print(stints_fp2)
tyre_types_fp3 , stints_fp3 = get_tyres_used("practice 3")
print(tyre_types_fp3)
print(stints_fp3)
tyre_types_quali , stints_quali = get_tyres_used("qualifying")
print(tyre_types_quali)
print(stints_quali)

tyre_types_all = [tyre_types_fp1, tyre_types_fp2, tyre_types_fp3, tyre_types_quali]
tyre_stints_all = [stints_fp1, stints_fp2, stints_fp3, stints_quali]
tyres_used = {"SOFT": [], 
            "MEDIUM": [], 
            "HARD": []}

for i in range(len(tyre_types_all)):
    for type in tyre_types_all[i]:
        for stint in tyre_types_all[i][type]:
            val = tyre_stints_all[i][stint][-1]
            print(val)
            tyres_used[type].append(val)

print(tyres_used)


tyres_avail = {"SOFT": [x + 1 for x in tyres_used["SOFT"]], 
            "MEDIUM": [x + 1 for x in tyres_used["MEDIUM"]], 
            "HARD": [x + 1 for x in tyres_used["HARD"]]}

for type in tyres_avail:
    for i in range(len(tyres_avail[type]), tyreAvailability[type]):
        tyres_avail[type].append(0)

        
print(tyres_avail)



print()
print()
print("RACE DATA")
print()
print()

session_race = fastf1.get_session(2022, 'hungary', 'race')
print(session_race.load())
print(session_race.laps.columns)
session_race_data = session_race.laps[["DriverNumber", "LapTime", "LapNumber", "PitOutTime", "PitInTime", "Compound", "TyreLife", "Stint", "IsAccurate"]]
print(session_race_data)
for index, lap in session_race_data.iterlaps():
    if lap["DriverNumber"] == driver:
        print(lap["LapTime"], " ", lap["LapNumber"], " ", lap["Compound"], " ", lap["TyreLife"], " ", lap["Stint"])

print(session_race_data[session_race_data["DriverNumber"] == driver])
x = []
y = []
z = []
stints = []
type_array = []
print()

stint_types = {"SOFT": [], "MEDIUM": [], "HARD": []} ## holds tyre type for each stint

for index, lap in session_race_data.iterlaps():
    if (lap["DriverNumber"] == driver and lap["IsAccurate"]):
        x.append(lap["TyreLife"])
        y.append(convert(lap["LapTime"]) + laptime_gained_per_lap*int(lap["LapNumber"]))
        z.append(int(lap["Stint"]))
        if (int(lap["Stint"]) not in stint_types[lap["Compound"]]):
            stint_types[lap["Compound"]].append(int(lap["Stint"]))
        # if(lap["Stint"] not in stint_types):
        #     stint_types[lap["Stint"]] = lap["Compound"]
print(stint_types)
## get stint data

stints = {}
for i in range(len(y)): 
    if z[i] not in stints:
        stints[z[i]] = [[x[i]] , [y[i]]]
    else:
        stints[z[i]][0].append(x[i])
        stints[z[i]][1].append(y[i])
        
print(stints)

# print(stints)

stint_info = aggregate_tyres(stints, stint_types)

x = [x for x in stint_info["SOFT"][0]]
y = [i/1000 for i in stint_info["SOFT"][1]]
plt.plot(x, y, color = "red", label = "SOFT",linewidth = 3)

x = [x for x in stint_info["MEDIUM"][0]]
y = [i/1000 for i in stint_info["MEDIUM"][1]]
plt.plot(x, y, color = "green", label = "MEDIUM",linewidth = 3)

x = [x for x in stint_info["HARD"][0]]
y = [i/1000 for i in stint_info["HARD"][1]]
plt.plot(x, y, color = "grey", label = "HARD",linewidth = 3)

if driver == "4":
    Name  = 'Norris'
elif driver == "16":
    Name = 'Leclerc'

# labels = ['Norris', 'Leclerc']


plt.title("Tyre Degradation - " + Name, fontsize=20)
plt.xlabel("Lap", fontsize=20)
plt.ylabel("Laptime (seconds)", fontsize=20)
plt.yticks(fontsize=20)
plt.xticks(fontsize=20)

plt.legend()
plt.tight_layout()

plt.savefig('TyreDegradation-Driver' + driver + '.png',bbox_inches='tight',dpi=1000,transparent=True)

info = []
for tyre_type in tyres_avail:
    for life in tyres_avail[tyre_type]:
        degradation = pd.DataFrame(stint_info[tyre_type][1][life:life+num_laps].T, columns = [tyre_type+ " "+str(life)])

        info.append(degradation)

info = pd.concat(info, axis = 1)
print(info)
info.to_csv("DATA/DRIVER" + driver + "/info.csv")

laptimes = [stint_info["SOFT"][1][0:70], stint_info["MEDIUM"][1][0:70], stint_info["HARD"][1][0:70]]

laptimes = np.array(laptimes)
laptimes = pd.DataFrame(laptimes)
laptimes.to_csv("DATA/DRIVER" + driver + "/laptimes.csv")
# print(laptimes)