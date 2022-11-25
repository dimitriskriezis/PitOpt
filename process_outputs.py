import matplotlib.pyplot as plt
import sys
from datetime import datetime
import pandas as pd
import matplotlib.dates
from scipy import stats
import numpy as np

optimalPitStopSchedule = np.loadtxt("OptimalPitStopSchedule.csv",delimiter=",")
print(optimalPitStopSchedule)

tyreScheduleSoft = np.loadtxt("SoftTyreUseSchedule.csv",delimiter=",")
print(tyreScheduleSoft)

tyreScheduleMedium = np.loadtxt("MediumTyreUseSchedule.csv",delimiter=",")
print(tyreScheduleMedium)

tyreScheduleHard = np.loadtxt("HardTyreUseSchedule.csv",delimiter=",")
print(tyreScheduleHard)

L = 70

List = []
PitStopLaps = []
for i in range(L):


    if optimalPitStopSchedule[i] == 1:
        PitStopLaps.append(i+1)

    if sum(tyreScheduleSoft[:,i]) == 1:
        List.append("S")
    
    if sum(tyreScheduleMedium[:,i]) == 1:
        List.append("M")

    if sum(tyreScheduleHard[:,i]) == 1:
        List.append("H")

print(List)
print(PitStopLaps)