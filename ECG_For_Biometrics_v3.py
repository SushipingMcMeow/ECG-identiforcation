# -*- coding: utf-8 -*-
"""
Created on Mon Oct 18 14:23:38 2021

@author: Alastair
"""

import pandas as pd
from sklearn.model_selection import train_test_split
import csv
import neurokit2 as nk
from neurokit2 import ecg_clean
import matplotlib.pyplot as plt
import numpy as np
import time
import random
import dtw
from os import listdir
from os.path import isfile, join
import copy
class profile:
    def __init__(self,ID,HBs):
        self.ID = ID
        self.HBs = HBs
class subject:
    def __init__(self,ID,HeartBeat):
        self.ID = ID
        self.HeartBeat = HeartBeat
class subjectScore:
    def __init__(self,ID,Score):
        self.ID = ID
        self.Score = Score
class finalRoundProfile:
    def __init__(self,ID,profileSubjects):
        self.ID = ID
        self.profileSubjects = profileSubjects
Dir = (".\CYBHi\data\long-term")
signal_freq = 1000
profileSize = 5
numOfProfiles = 30
#selects a random allotment of data from the provided data array
def shrinkTo(data,amount):
    cutoff = random.randint(0,len(data) - amount-1)
    data = np.resize(data,cutoff+amount)
    cutoffIndex = np.arange(cutoff)
    data = np.delete(data,cutoffIndex)
    return data
#Imports a random set of test files from the directory
def importfiles(amount):
    returnFiles = []
    filenames = [f for f in listdir(Dir) if isfile(join(Dir, f))]
    while (len(returnFiles) < amount):
        fileInQ = filenames[random.randint(0,len(filenames)-1)]
        if fileInQ not in returnFiles:
            returnFiles.append(fileInQ)
    return returnFiles
#gets the data from a specified file
def getData(fileName):
    ecg_signal = np.loadtxt(Dir+"\\"+fileName)    
    ecg_signal = ecg_clean(ecg_signal, signal_freq)
    fileName = fileName[:-4]
    return ecg_signal
 #generates a set of profile objects each with the ID of it's source file and a number of heart beats equivelant to profileSize
def subjectArray(data):
    newProfiles = []
    for i in range(len(data)):
        thing = profile(data[i][:-4],getHeatBeats(getData(data[i]),profileSize))
        #thing = i*i
        newProfiles.append(copy.deepcopy(thing))
        print(newProfiles[i].ID)
    return newProfiles
#selects a heart beat range from 1 specified r peak to the next in a data sequence.
def rpeakToRpeak(data,rpeaks, rpeak):
    data = data[rpeaks[rpeak]:rpeaks[rpeak+1]]
    return data
#selects a single random heart beat from a data sequence.
def singleHB(data):
        dataFrag=shrinkTo(data,5000)
        ecg_clean(dataFrag)
        _, rpeaks = nk.ecg_peaks(dataFrag, sampling_rate=signal_freq)
        return rpeakToRpeak(dataFrag,rpeaks['ECG_R_Peaks'],1)
#returns a list of random heart beats from a sequence
def getHeatBeats(data,amount):
    heartBeats = []
    for i in range(amount):
        heartBeats.append(singleHB(data))
    return heartBeats
#generates a single subject object with an ID and heartbeat
def generateSubject(fileName):
    return subject(fileName[:-4],singleHB(getData(fileName)))
def runTest(participants,testSubject,questionSubject):
    topScoringSubs = []
    topScoringProfiles = []
    #generates the score for each entry then selects the 5 lowest scores
    for i in range(len(participants)):
        for e in range(len(participants[i].HBs)):
            testDTW = dtw(participants[i].HBs[e],testSubject.HBs)
            testWA = dtw.warpArea(testDTW)
            if (len(topScoringSubs) < 5):
                topScoringSubs.append(subjectScore(participants[i].ID,testWA))
                topScoringSubs.sort(key=lambda x: x.Score, reverse=True)
            else:
                for x in range(len(topScoringSubs)):
                    if (testWA < topScoringSubs[x].Score):
                        topScoringSubs[x] = subjectScore(participants[i],testWA)
                        break
    #groups the 5 scores by ID
    for i in range(len(topScoringSubs)):
        if len(topScoringProfiles) != 0:
            thing = []
            thing.append(topScoringSubs[i])
            topScoringProfiles.append(finalRoundProfile(topScoringSubs[i].ID,thing))
        elif (any(x.ID == topScoringSubs[i].ID for x in topScoringProfiles)):
            for e in range(len(topScoringProfiles)):
                if (topScoringProfiles[e].ID == topScoringSubs[i]):
                    topScoringProfiles[e].profileSubjects.append(topScoringSubs[i])
        else:
            topScoringProfiles.append(finalRoundProfile(topScoringSubs[i].ID,thing))
    topScoringProfiles.sort(key = lambda x: len(x.profileSubjects))
    if len(topScoringProfiles[0].profileSubjects) ==
            
            
            

data = importfiles(numOfProfiles)
subjectData = subjectArray(data)
for i in range(len(subjectData)):
    plt.plot(subjectData[i].HBs[2])