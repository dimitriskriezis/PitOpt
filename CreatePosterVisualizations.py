import matplotlib.pyplot as plt
import sys
from datetime import datetime
import pandas as pd
import matplotlib.dates
from scipy import stats
import numpy as np
import csv
import os
from matplotlib.patches import Patch

drivers = [4,16]

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

# create a column with the color for each department
def color(row):
    c_dict = {'SOFT 0':'#E64646', 'HARD 0':'#E69646', 'MEDIUM 0':'#34D05C', 'SOFT 4':'#34D0C3', 'IT':'#3475D0'}
    return c_dict[row['Tyre']]


def AppendToDataFrame(driverNumber,df,Name):
    pitStopSchedule = GetPitStopSchedule(driverNumber)
    tyreSchedule = GetTyreSchedule(driverNumber)
    l = pitStopSchedule.copy()
    l.insert(0,0)
    x = [tyreSchedule[x-1] for x in l]
    pitStopSchedule.append(70)
    for count, value in enumerate(pitStopSchedule):
        print(count)
        df.loc[len(df.index)] = [Name + " Optimized",x[count],l[count],pitStopSchedule[count],pitStopSchedule[count] - l[count]]

def AppendToDataFrameReal(driverNumber,df,Name):
    pitStopSchedule = GetRealPitStopSchedule(driverNumber)
    tyreSchedule = GetRealTyreSchedule(driverNumber)
    l = pitStopSchedule.copy()
    l.insert(0,0)
    x = [tyreSchedule[x-1] for x in l]
    pitStopSchedule.append(70)
    for count, value in enumerate(pitStopSchedule):
        print(count)
        df.loc[len(df.index)] = [Name + " Real",x[count],l[count],pitStopSchedule[count],pitStopSchedule[count] - l[count]]



df  = pd.DataFrame(columns = ['Driver','Tyre','Start','Stop','Duration'])

AppendToDataFrame(4,df,'Norris -')
AppendToDataFrame(16,df,'Leclerc -')
AppendToDataFrameReal(4,df,'Norris -')
AppendToDataFrameReal(16,df,'Leclerc -')

print(df)

df = df.sort_values('Driver')

print(type(df['Tyre'][0]))

c_dict = {'SOFT 4':'#E64646', 'HARD 0':'#E69646', 'MEDIUM 0':'#34D05C', 'SOFT 0':'#34D0C3'}
legend_elements = [Patch(facecolor=c_dict[i], label=i)  for i in c_dict]

df['color'] = df.apply(color, axis=1)

fig, ax = plt.subplots(1, figsize=(16,6))
ax.barh(df.Driver, df.Duration, left=df.Start,color=df.color,edgecolor = 'black')

plt.xticks(fontsize=20)
plt.yticks(fontsize=20)

ax.set_xlabel('Lap Number',fontsize=20)
ax.set_xlim(0,90)

plt.title('Real vs Optimized Tyre Schedules',fontsize=20)

plt.legend(loc="upper right",handles=legend_elements,fontsize=20)

plt.savefig('TyreScheduleComparison.png',bbox_inches='tight',dpi=1000,transparent=True)

# plt.show()
