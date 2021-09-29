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
def selectRpeakRange(data,rpeaks,ppeaks, tpeaks):
    RPeakA = random.randint(1, len(ppeaks)-1)
    RPeakB = -1
    while(RPeakB == -1):
        newRPeak = random.randint(1,len(rpeaks)-1)
        if (newRPeak != RPeakA):
            RPeakB = newRPeak
#gets data between both P peaks surounding an R peak
def selectHeartBeat(data, rpeak, ppeaks):
    ppeakInQuestion = len(ppeaks) - 1
    ppeaka = -1
    while(ppeaka == -1):
        if (ppeaks[ppeakInQuestion] < rpeak):
            ppeaka = ppeakInQuestion
        else:
            ppeakInQuestion -= 1
    ppeakb = -1
    ppeakInQuestion = 0
    while(ppeakb == -1):
        if (ppeaks[ppeakInQuestion] > rpeak):
            ppeakb = ppeakInQuestion
            print("ppeak in question",ppeaks[ppeakInQuestion])
        else:
            ppeakInQuestion += 1
    data = data[ppeaks[ppeaka]:-(len(data)-ppeaks[ppeakb])]
    print("selected heart beat length: ",len(data))
    return data
    

sampling_freq=1000
ecg_signal=np.loadtxt(".\CYBHi\data\long-term\\20120430-PES-A0-35.txt")
ecg_signal = shrinkTo(ecg_signal,10000)
ecg_signal_cleared = ecg_clean(ecg_signal, sampling_freq)
#ecg_signal = ecg_signal_cleared
#ecg_signal=np.loadtxt("20120106-AA-A0-35_small.txt")

ecg_signal_short=ecg_signal[:100]
timestr = time.strftime("%Y%m%d-%H%M%S")

_, rpeaks = nk.ecg_peaks(ecg_signal, sampling_rate=sampling_freq)
signals, waves_peak = nk.ecg_delineate(ecg_signal, rpeaks, sampling_rate=sampling_freq)
signals, info = nk.ecg_process(ecg_signal, sampling_rate=sampling_freq)
rndhb = selectHeartBeat(ecg_signal_cleared, rpeaks['ECG_R_Peaks'][3],waves_peak['ECG_P_Peaks'])
print("rpeak type is",rpeaks)
print(type(signals))
print(len(signals))
print(signals)
print(ecg_signal)
print(len(ecg_signal))
print(waves_peak)
print("selected heart beat:", rndhb)
plotb = plt.plot(rndhb)
plot = nk.events_plot([waves_peak['ECG_T_Peaks'],
                       waves_peak['ECG_P_Peaks'],
                       waves_peak['ECG_Q_Peaks'],
                       waves_peak['ECG_S_Peaks']], ecg_signal_cleared)

_, rpeaks = nk.ecg_peaks(ecg_signal, sampling_rate=sampling_freq)