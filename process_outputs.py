import matplotlib.pyplot as plt
import sys
from datetime import datetime
import pandas as pd
import matplotlib.dates
from scipy import stats
import numpy as np
import csv
import os

def LoadSchedule(FileName):
    tyreSchedule = np.loadtxt(FileName,delimiter=",")
    return tyreSchedule

driverNumber = 16

TyreNames = []
with open('DATA/DRIVER' + str(driverNumber) + '/info.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    row = next(csv_reader)
    for i in range(13):
        TyreNames.append(row[i+1])


optimalPitStopSchedule = np.loadtxt('DATA/DRIVER' + str(driverNumber) + '/OptimalPitStopSchedule.csv',delimiter=",")
print(optimalPitStopSchedule)

FileNames = ['DATA/DRIVER' + str(driverNumber) + '/Tyre-' + str(x) + '.csv' for x in range(1,14,1)]
TyreSchedules = [LoadSchedule(FileName) for FileName in FileNames]


L = 70

TyreList = []
PitStopLaps = []
for i in range(L):


    if optimalPitStopSchedule[i] == 1:
        PitStopLaps.append(i+1)

    for j in range(13):
        if sum(TyreSchedules[j][:,i]) == 1:
            TyreList.append(TyreNames[j])

print(TyreList)
print(PitStopLaps)
print(len(TyreList))

csvFileName = 'DATA/DRIVER' + str(driverNumber) + '/TyreSchedule.csv'
if os.path.exists(csvFileName):
    os.remove(csvFileName)
with open(csvFileName, 'w', newline='') as myfile:
     wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
     wr.writerow(TyreList)

csvFileName = 'DATA/DRIVER' + str(driverNumber) + '/PitStopSchedule.csv'
if os.path.exists(csvFileName):
    os.remove(csvFileName)
with open(csvFileName, 'w', newline='') as myfile:
     wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
     wr.writerow(PitStopLaps)