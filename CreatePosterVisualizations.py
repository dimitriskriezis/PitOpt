import matplotlib.pyplot as plt
import sys
from datetime import datetime
import pandas as pd
import matplotlib.dates
from scipy import stats
import numpy as np
import csv
import os

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

pitStopSchedule = GetPitStopSchedule(4)
tyreSchedule = GetTyreSchedule(4)

l = pitStopSchedule.copy()
l.insert(0,0)
x = [tyreSchedule[x-1] for x in l]

pitStopSchedule.append(70)
print(x)
print(pitStopSchedule)

# fig = plt.figure()
# ax = fig.add_subplot(111)
# jobs = ["1","2","3"]
# ax.barh(jobs, pitStopSchedule, align='center', height=.25, color='#00ff00',label='wait time')
# plt.show()
