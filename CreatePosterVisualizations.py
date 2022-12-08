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

def GetTyreSchedule(driverNumber):
    row = []
    with open('DATA/DRIVER' + str(driverNumber) + '/TyreSchedule.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        row = [x for x in next(csv_reader)]
    return row

driverNumber = 4
pitStopSchedule = GetPitStopSchedule(driverNumber)
tyreSchedule = GetTyreSchedule(driverNumber)

l = pitStopSchedule.copy()
l.insert(0,0)
x = [tyreSchedule[x-1] for x in l]

pitStopSchedule.append(70)
print(x)
print(l)
print(pitStopSchedule)

df  = pd.DataFrame(columns = ['Driver','Tyre','Start','Stop','Duration'])
for count, value in enumerate(pitStopSchedule):
    print(count)
    df.loc[len(df.index)] = ["Driver" + str(driverNumber),x[count],l[count],pitStopSchedule[count],pitStopSchedule[count] - l[count]]

print(df)

# create a column with the color for each department
def color(row):
    c_dict = {'SOFT 0':'#E64646', 'HARD':'#E69646', 'MEDIUM 0':'#34D05C', 'SOFT 4':'#34D0C3', 'IT':'#3475D0'}
    return c_dict[row['Tyre']]

c_dict = {'SOFT 4':'#E64646', 'HARD':'#E69646', 'MEDIUM 0':'#34D05C', 'SOFT 0':'#34D0C3', 'IT':'#3475D0'}
legend_elements = [Patch(facecolor=c_dict[i], label=i)  for i in c_dict]

df['color'] = df.apply(color, axis=1)

fig, ax = plt.subplots(1, figsize=(16,6))
ax.barh(df.Driver, df.Duration, left=df.Start,color=df.color,edgecolor = 'black')


plt.legend(handles=legend_elements)


plt.show()
