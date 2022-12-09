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

def GetPitStopSchedule(driverNumber):
    row = []
    with open('DATA/DRIVER' + str(driverNumber) + '/PitStopSchedule.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        row = [int(x) for x in next(csv_reader)]
    return row

def GetRealPitStopSchedule(driverNumber):
    row = []
    with open('DATA/DRIVER' + str(driverNumber) + '/RealPitStopSchedule.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        row = [int(x) for x in next(csv_reader)]
    return row

def GetRealTyreSchedule(driverNumber):
    row = []
    with open('DATA/DRIVER' + str(driverNumber) + '/RealTyreSchedule.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        row = [x for x in next(csv_reader)]
    return row

def GetTyreSchedule(driverNumber):
    row = []
    with open('DATA/DRIVER' + str(driverNumber) + '/TyreSchedule.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        row = [x for x in next(csv_reader)]
    return row

def GetSummation(pitStopSchedule,tyreSchedule):
    
    if isinstance(pitStopSchedule,str):
        pitStopSchedule = [int(pitStopSchedule)]

    df = pd.read_csv("DATA/DRIVER" + str(driverNumber) + "/laptimes.csv", index_col=[0])
    subsequentLap = 0
    currentTyre = "Dummy"
    LapNum = []
    StartingIndex = {"MEDIUM 0": 0, "HARD 0": 0, "SOFT 0":0, "SOFT 4": 3}
    GlobalTyreIndex = {"MEDIUM 0": 1, "HARD 0": 2, "SOFT 0":0, "SOFT 4": 0}
    summation = 0
    for count,val in enumerate(tyreSchedule):
        if (val != currentTyre) | (pitStopSchedule.count(count+1)):
            subsequentLap = StartingIndex[val]
            LapNum.append(subsequentLap)
            currentTyre = val
        else:
            LapNum.append(subsequentLap)
        tyreInd = GlobalTyreIndex[val]
        summation += df.iloc[tyreInd][subsequentLap]
        subsequentLap = subsequentLap + 1
    summation += len(pitStopSchedule)*22000
    return summation

driverNumber = 16
pitStopSchedule = GetPitStopSchedule(driverNumber)
tyreSchedule = GetTyreSchedule(driverNumber)
cumTime16 = GetSummation(pitStopSchedule,tyreSchedule)/1000
print(cumTime16)

driverNumber = 16
pitStopSchedule = GetRealPitStopSchedule(driverNumber)
tyreSchedule = GetRealTyreSchedule(driverNumber)
cumTime16Real = GetSummation(pitStopSchedule,tyreSchedule)/1000
print(cumTime16Real)

driverNumber = 4
pitStopSchedule = GetPitStopSchedule(driverNumber)
tyreSchedule = GetTyreSchedule(driverNumber)
cumTime4 = GetSummation(pitStopSchedule,tyreSchedule)/1000
print(cumTime4)

driverNumber = 4
pitStopSchedule = GetRealPitStopSchedule(driverNumber)
tyreSchedule = GetRealTyreSchedule(driverNumber)
cumTime4Real = GetSummation(pitStopSchedule,tyreSchedule)/1000
print(cumTime4Real)

import matplotlib.pyplot as plt
import numpy as np


labels = ['Driver 4', 'Driver 16']
real = [cumTime4Real, cumTime16Real]
opt = [cumTime4, cumTime16]

x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, real, width, label='Real')
rects2 = ax.bar(x + width/2, opt, width, label='Optimized')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Sprint Duration (seconds)',fontsize=20)
ax.set_title('Sprint Duration - Real vs Optimized',fontsize=20)
ax.set_xticks(x, labels,fontsize=20)
plt.yticks(fontsize=20)
ax.set_ylim(0,8000)
ax.legend(loc="upper right",fontsize=10)


ax.bar_label(rects1, padding=3)
ax.bar_label(rects2, padding=3)

fig.tight_layout()

plt.savefig('SprintDurationComparison.png',bbox_inches='tight',dpi=1000,transparent=True)


# plt.show()