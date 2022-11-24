import fastf1
import matplotlib.pyplot as plt
import sys
from datetime import datetime
import pandas as pd
import matplotlib.dates
from scipy import stats
import numpy as np

def convert(td):
    print(td.components)
    time = td.components.minutes*60 + td.components.seconds
    time = time * 1000 + td.components.milliseconds
    return time

# fastf1.Cache.enable_cache('path/to/cache/')  

fuelCapacity = 110
num_laps = 70
fuel_per_lap = fuelCapacity/num_laps
laptime_per_kg_of_fuel = 0.03 * 1000 # milliseconds
laptime_gained_per_lap = laptime_per_kg_of_fuel * fuel_per_lap


session = fastf1.get_session(2022, 'hungary', 'race')
print(session.load())
print(session.laps.columns)
session_data = session.laps[["DriverNumber", "LapTime", "LapNumber", "PitOutTime", "PitInTime", "Compound", "TyreLife", "Stint", "IsAccurate"]]
print(session_data)
for index, lap in session_data.iterlaps():
    if lap["DriverNumber"] == "16":
        print(lap["LapTime"], " ", lap["LapNumber"], " ", lap["Compound"], " ", lap["TyreLife"], " ", lap["Stint"])

print(session_data[session_data["DriverNumber"] == '16'])
x = []
y = []
z = []
stints = []
print()

for index, lap in session_data.iterlaps():
    if (lap["DriverNumber"] == '16' and lap["IsAccurate"]):
        x.append(lap["LapNumber"])
        y.append(convert(lap["LapTime"]) + laptime_gained_per_lap*int(lap["LapNumber"]))
        z.append(int(lap["Stint"]))


stints = {}
for i in range(len(y)): 
    if z[i] not in stints:
        stints[z[i]] = [([x[i]], [y[i]])]
    else:
        tup = (x[i], y[i])
        stints[z[i]].append(tup)
        

print(stints)

for stint in stints:
    stints[stint].pop(0)
    start_lap = min(stints[stint])[0]
    for i in range(len(stints[stint])):
        new_pair = (stints[stint][i][0] - start_lap + 1, stints[stint][i][1])
        stints[stint][i] = new_pair
    

stint1_x = [tup[0] for tup in stints[1]]
stint1_y = [tup[1] for tup in stints[1]]


slope, intercept, r, p, std_err = stats.linregress(stint1_x, stint1_y)
def myfunc(x):
  return slope * x + intercept


indices = [i for i in range(1, 71)]

mymodel1 = list(map(myfunc, indices))
print("stint1 slop", slope)

stint3_x = [tup[0] for tup in stints[3]]
stint3_y = [tup[1] for tup in stints[3]]
slope, intercept, r, p, std_err = stats.linregress(stint3_x, stint3_y)
print("stint3 slope", slope)

def myfunc(x):
  return slope * x + intercept
mymodel3 = list(map(myfunc, indices))

stints[4].pop()
stint4_x = [tup[0] for tup in stints[4]]
stint4_y = [tup[1] for tup in stints[4]]
slope, intercept, r, p, std_err = stats.linregress(stint4_x, stint4_y)
print("stint4 slope", slope)

def myfunc(x):
  return slope * x + intercept
mymodel4 = list(map(myfunc, indices))

plt.plot(stint1_x, stint1_y, 'o', color = "blue")
plt.plot(indices, mymodel1, color = "blue")

plt.plot(stint3_x, stint3_y, 'o', color = "red")
plt.plot(indices, mymodel3, color = "red")

plt.plot(stint4_x, stint4_y, 'o', color = "green")
plt.plot(indices, mymodel4, color = "green")
# plt.show()

laptimes = [mymodel4, mymodel1, mymodel3]

laptimes = np.array(laptimes)
laptimes = pd.DataFrame(laptimes)
laptimes.to_csv("laptimes.csv")
print(laptimes)