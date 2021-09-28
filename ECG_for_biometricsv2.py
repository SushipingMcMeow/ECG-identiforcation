# -*- coding: utf-8 -*-
"""
Created on Sun Sep  5 17:22:01 2021

@author: Alastair
"""

import neurokit2 as nk
from neurokit2 import ecg_clean
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time
import statistics
from statistics import mean
import random
import bisect
import os
import dtw
from dtw import *


#shirinks a data set down to a specified amount
def shrinkTo(data,amount):
    cutoff = random.randint(0,len(data) - amount-1)
    data = np.resize(data,cutoff+amount)
    cutoffIndex = np.arange(cutoff)
    data = np.delete(data,cutoffIndex)
    print("new data length:", len(data))
    return data
#testing method used to select two different heart beats in a sequence
def selectHeartBeats(data,rpeaks,ppeaks, tpeaks):
    RPeakA = random.randint(1, len(rpeaks)-1)
    RPeakB = -1
    while(RPeakB == -1):
        newRPeak = random.randint(1,len(rpeaks)-1)
        if (newRPeak != RPeakA):
            RPeakB = newRPeak
    
    
sampling_freq=500
ecg_signal=np.loadtxt(".\CYBHi\data\long-term\\20120430-PES-A0-35.txt")
ecg_signal = shrinkTo(ecg_signal,10000)
ecg_signal_cleared = ecg_clean(ecg_signal, sampling_freq)
ecg_signal = ecg_signal_cleared
#ecg_signal=np.loadtxt("20120106-AA-A0-35_small.txt")

ecg_signal_short=ecg_signal[:100]
timestr = time.strftime("%Y%m%d-%H%M%S")
#plt.plot(ecg_signal[:200])
#plt.plot(ecg_signal_short)
#plt.savefig(timestr+'.jpg',format='jpg', dpi=300)

_, rpeaks = nk.ecg_peaks(ecg_signal, sampling_rate=sampling_freq)
signals, waves_peak = nk.ecg_delineate(ecg_signal, rpeaks, sampling_rate=sampling_freq)
plt(ecg_signal_cleared)
plt(ecg_signal)

signals, info = nk.ecg_process(ecg_signal, sampling_rate=sampling_freq)
print("rpeak type is",rpeaks)
print(type(signals))
print(len(signals))
print(signals)
print(ecg_signal)
print(len(ecg_signal))
plot = nk.events_plot(rpeaks['ECG_R_Peaks'], ecg_signal_cleared)

_, rpeaks = nk.ecg_peaks(ecg_signal, sampling_rate=sampling_freq)