#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 25 11:51:11 2021

@author: ambi
"""

# Load NeuroKit and other useful packages
import neurokit2 as nk
from neurokit2 import ecg_clean
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time
import statistics
from sklearn import preprocessing
from sklearn.preprocessing import normalize
from statistics import mean
import random
import os
import bisect
from statsmodels.nonparametric.smoothers_lowess import lowess
from scipy.signal import savgol_filter

#%matplotlib inline
#plt.rcParams['figure.figsize'] = [8, 5]  # Bigger images
def findIQR(data):
    data.sort()
    IQR = data[5]-data[2]
    return IQR
#normalises all values so all data is in between -1 and 1 while the average is 0
def normalizeAttempt(data):
    newdata = data.tolist()
    avg = mean(newdata)
    print("before max ",max(newdata)," mean ",avg)
    for i in newdata:
        i = i - avg
    MaxMin = 0
    if min(newdata) < -max(newdata):
        MaxMin = min(newdata)
        print("minmax ", MaxMin)
        for i in range(len(newdata)):
            newdata[i] = newdata[i]/MaxMin
    else:
        MaxMin = max(newdata)
        print("minmax ", MaxMin)
        for i in range(len(newdata)):
            newdata[i] = newdata[i]/MaxMin
    
    print("post max ",max(newdata))
    newnewdata = np.array(newdata)
    print(newnewdata)
    return newnewdata
#smooth ecg data code from https://www.delftstack.com/howto/python/smooth-data-in-python/#use-the-numpy.convolve-method-to-smooth-data-in-python
def smooth(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth
#shirinks a data set down to a specified amount
def shrinkTo(data,amount):
    cutoff = random.randint(0,len(data) - amount-1)
    data = np.resize(data,cutoff+amount)
    cutoffIndex = np.arange(cutoff)
    data = np.delete(data,cutoffIndex)
    print("new data length:", len(data))
    return data

#gets a sequence of numbers and turns it into intervals
def makeIntervals(sequence):
    sequenceIntervals = []
    for i in range(len(sequence)-1):
        sequenceIntervals.append(sequence[i+1] - sequence[i])
    return sequenceIntervals
#averages out each point over the the nuber of points equal to the level to help mitigate noise
def noiseReduction(data,level):
    newdata = np.array([sum(data[0:level])/level])
    for i in range(1,len(data)-level):
        newdata = np.append(newdata,sum(data[i:i+level])/level)
    print("some data:",newdata)
    print("some data length:",len(newdata))
    return newdata
#turns PQRST data into vectors
def makeHeartBeatsArray(p,q,r,s,t,data):
    returnData = np.Array([])
    for i in range(1,len(r)-1):
        Ap = bisect.bisect_left(p,r[i])
        Aq = bisect.bisect_left(q,r[i])
        As = bisect.bisect_right(s,r[i])
        At = bisect.bisect_right(t,r[i])
        Bp = data[Aq] - data[Ap]
        Bq = data[r[i]] - data[Aq]
        Br = data[As]-data[r[i]]
        Bs = data[At]-data[As]
#ecg_signal=np.loadtxt("X_train_first_ECG_short.csv")
#sampling_freq=360
#f = open(os.getcwd() + "\CYBHi\data\long-term")
#print(np.loadtxt(".\CYBHi\data\long-term\\20120106-AA-A0-35.txt"))
#ecg_signal=np.loadtxt("ECG_Signal_test1_100_Sample_per_second_10_Second_Data.txt")
ecg_signal=np.loadtxt(".\CYBHi\data\long-term\\20120427-MMJ-A0-35.txt")

#ecg_signal=np.loadtxt("20120106-AA-A0-35_small.txt")
#ecg_signal = normalize(ecg_signal)
ecg_signal = shrinkTo(ecg_signal,5000)
n1 = ecg_signal/np.linalg.norm(ecg_signal)
n2 = noiseReduction(ecg_signal,20)
#n31 = np.concatenate((ecg_signal,np.arange(0,len(ecg_signal))), axis=0)
#n3 = lowess(n2,np.arange(0,len(n2)),frac=0.001)
#n3 = savgol_filter(n1,51,3)
#n3 = smooth(ecg_signal, 9)
n3 = nk.ecg_clean(ecg_signal,sampling_rate=500,method="neurokit")
plt.plot(n3)
#ecg_signal = n3
print("new ecg signals are",n3)
print("new ecg signal type",type(n3))

#ecg_signal_short = ecg_signal[:5000]
timestr = time.strftime("%Y%m%d-%H%M%S")
#plt.plot(ecg_signal[:200])
#plt.plot(ecg_signal_short)
plt.savefig(timestr+'.jpg',format='jpg', dpi=300)

sampling_freq=500

signals, info = nk.ecg_process(ecg_signal, sampling_rate=sampling_freq)
#for i in range(0,len(signals) -1000 ):
 #   signals.pop()
print(type(signals))
print(len(signals))
print("signals are",signals)

print("**************",type(info))
print("**************",info)


# Extract R-peaks locations
#_, rpeaks = nk.ecg_peaks(ecg_signal, sampling_rate=3000)
_, rpeaks = nk.ecg_peaks(ecg_signal, sampling_rate=sampling_freq)

# Delineate
#signal, waves = nk.ecg_delineate(ecg_signal, rpeaks, sampling_rate=3000, method="dwt", show=True, show_type='all')
signal, waves = nk.ecg_delineate(ecg_signal, rpeaks, sampling_rate=sampling_freq, method="dwt", show=True, show_type='all')


#_, waves_peak = nk.ecg_delineate(ecg_signal, rpeaks, sampling_rate=sampling_freq)
signals1, waves_peak = nk.ecg_delineate(ecg_signal, rpeaks, sampling_rate=sampling_freq)
#signals1, waves_peak = nk.ecg_delineate(ecg_signal, rpeaks, sampling_rate=sampling_freq, show=True, show_type='peaks')
#fig1=nk.ecg_plot(signals1, sampling_rate=sampling_freq)
#fig1.savefig("hh.jpg",format='jpg', dpi=200)
#rpeakIntervals = makeIntervals(rpeaks['ECG_R_Peaks'])
#rpeakIntervals = shrinkToEight(rpeakIntervals)
#rpeakIQR = findIQR(rpeakIntervals)
#rpeakIntRange = range(rpeakIntervals)
#for i in range(len(rpeaks['ECG_R_Peaks']) - 1):
#    rpeakIntervals.append(rpeaks['ECG_R_Peaks'][i+1] - rpeaks['ECG_R_Peaks'][i])
    
timestr = time.strftime("%Y%m%d-%H%M%S")
fig=nk.ecg_plot(signals, sampling_rate=sampling_freq)
fig.savefig("ff_"+timestr+"_.jpg",format='jpg', dpi=200)
#fig.savefig("ee.jpg", dpi=100)
print("&&&&&&&&&&&&&&&", type(fig))

fileName="qqqq_"+"important_points_"+timestr
plt.savefig(fileName+'.jpg',format='jpg', dpi=200)

plt.figure(0)
plt.plot(ecg_signal)
plt.figure(1)
# Visualize the T-peaks, P-peaks, Q-peaks and S-peaks
plot = nk.events_plot([waves_peak['ECG_T_Peaks'],
                       waves_peak['ECG_P_Peaks'],
                       waves_peak['ECG_Q_Peaks'],
                       waves_peak['ECG_S_Peaks']], n3)
fileName2="uuuuuuuuuu_"+timestr
plot.savefig(fileName2+'.jpg',format='jpg', dpi=200)
print("*************** ecg_signal", ecg_signal)
print("*************** type(signal):[",type(signal),"]")
print("*************** signal",signal)

print("*************** type(waves)",type(waves))
print("*************** waves",waves)

print("*************** type(rpeaks)",type(rpeaks))
print("*************** type(rpeaks['ECG_R_Peaks'])",type(rpeaks['ECG_R_Peaks']))

print("*************** rpeaks",rpeaks)

#print("*************** rpeak intervals",rpeakIntervals)
#print("*************** rpeak IQR", rpeakIQR)
#print("*************** rpeak interval range", rpeakIntRange)

