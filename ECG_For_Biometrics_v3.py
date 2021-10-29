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
from dtw import *
from os import listdir
from os.path import isfile, join
import copy
from heapq import nsmallest
class profile:
    def __init__(self,ID,HBs):
        self.ID = ID
        self.HBs = HBs
class subject:
    def __init__(self,ID,HeartBeat):
        self.ID = ID
        self.HeartBeat = HeartBeat
Dir = (".\CYBHi\data\long-term")
signal_freq = 1000 #signal frequency used by the dataset 1000 for CYBHi
profilesize = 10 #number of heart beats to compare within a profile
numOfProfiles = 40 #number of profiles to be tested
numOfTests = 200 #number of test to be conducted
#selects a random allotment of data from the provided data array
def shrinkTo(data,amount):
    cutoff = random.randint(0,len(data) - amount-1)
    data = np.resize(data,cutoff+amount)
    cutoffIndex = np.arange(cutoff)
    data = np.delete(data,cutoffIndex)
    return data
#Imports a random set of test files from the directory
def importFiles(amount):
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
 #generates a set of profile objects each with the ID of it's source file and a number of heart beats equivelant to profilesize
def subjectArray(data):
    newprofiles = []
    for i in range(len(data)):
        thing = profile(data[i][:-4],getHeatBeats(getData(data[i]),profilesize))
        #thing = i*i
        newprofiles.append(copy.deepcopy(thing))
        print(newprofiles[i].ID)
    return newprofiles
#selects a heart beat range from 1 specified r peak to the next in a data sequence.
def rpeakToRpeak(data,rpeaks, rpeak):
    data = data[rpeaks[rpeak]:rpeaks[rpeak+1]]
    return data
#selects a single random heart beat from a data sequence.
def singleHB(data):
        dataFrag=shrinkTo(data,10000)
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
    topScoringprofiles = []
    PID, score = len(participants)*profilesize, 2
    profiles = [[0 for x in range(score)]for y in range(PID)]
    bestScore = None
    for i in range(len(participants)):
        for e in range(len(participants[i].HBs)):
            testDTW = dtw(participants[i].HBs[e],testSubject.HeartBeat)
            testWA = warpArea(testDTW)
            profiles[i*profilesize + e][1] = participants[i].ID
            profiles[i*profilesize + e][0] = testWA
    topProfiles = nsmallest(5,profiles)
    print(topProfiles)
    topProfileCounts = [[0 for x in range(2)]for y in range(1)]
    for i in range(len(topProfiles)):
        #first
        if i == 0:
            topProfileCounts[0][1] = topProfiles[0][1]
            topProfileCounts[0][0] += 1
        # if there's already an ID hit
        elif (topProfiles[i][1] in [e[1] for e in topProfileCounts]):
            topProfileCounts[[e[1] for e in topProfileCounts].index(topProfiles[i][1])][0] += 1
        #if it's a new ID hit
        else:
            topProfileCounts.append([1,topProfiles[i][1]])
    topProfileCounts = sorted(topProfileCounts, key=lambda x: x[0], reverse=True)
    if len(topProfileCounts) == 1:
        bestScore = topProfileCounts[0][1]
        print("single scoring profile event happend")
    #checks for score ties
    elif topProfileCounts[0][0] == 2 and topProfileCounts[1][0] == 2:
        print('tie event happend')
        bestScore = topProfiles[0][1]
    elif len(topProfileCounts)==5:
        print("5 different profiles event happend")
        bestScore = topProfiles[0][1]
    else:
        print("clear winner event happend")
        bestScore = topProfileCounts[0][1]
    print("best score is", bestScore)
    print("test subject is", testSubject.ID)
    print("subject in question", questionSubject)
    #returning true positive
    if (testSubject.ID == questionSubject) and (questionSubject == bestScore):
        return "TP"
    #returning false negative
    if (testSubject.ID == questionSubject) and (questionSubject != bestScore):
        return "FN"
    #returning true negative
    if (testSubject.ID != questionSubject) and (questionSubject != bestScore):
        return "TN"
    #return false positive
    if (testSubject.ID != questionSubject) and (questionSubject == bestScore):
        return "FP"
print("getting data")
data = importFiles(numOfProfiles)
print("converting file data")
subjectData = subjectArray(data)
summaryMatrix = [[0 for x in range(2)]for y in range(2)]
#testing
print("running tests")
for i in range(len(subjectData)):
    plt.plot(subjectData[i].HBs[2])
for i in range(numOfTests):
    print("test number", i+1)
    results = None
    #should return a TN or FP
    if (i % 2) == 0:
        n = random.sample(range(0,len(subjectData)-1),2)
        results = runTest(subjectData,generateSubject(data[n[0]]),data[n[1]][:-4])
    #should return a TP or FN
    else:
        n = random.randint(0,len(subjectData)-1)
        results = runTest(subjectData,generateSubject(data[n]),data[n][:-4])
    print(results)
    #tp
    if results == "TP":
        summaryMatrix[0][0] += 1
    #tn
    elif results == "TN":
        summaryMatrix[1][1] += 1
    #fp
    elif results == "FP":
        summaryMatrix[0][1] += 1
    #fn
    else:
        summaryMatrix[1][0] += 1
print("compiling results")
precision = summaryMatrix[0][0] / (summaryMatrix[0][0]+summaryMatrix[0][1])
negativePredictiveValue = summaryMatrix[1][1]/ (summaryMatrix[1][0]+summaryMatrix[1][1])
sensitivity = summaryMatrix[0][0]/(summaryMatrix[0][0]+summaryMatrix[1][0])
specificity = summaryMatrix[1][1]/(summaryMatrix[1][1]+summaryMatrix[0][1])
recall = summaryMatrix[0][0]/(summaryMatrix[0][0]+summaryMatrix[1][0])
FMeasure = (2*recall*precision)/(recall + precision)
accuracy = (summaryMatrix[0][0] + summaryMatrix[1][1])/(summaryMatrix[0][0]+summaryMatrix[1][1]+summaryMatrix[1][0]+summaryMatrix[0][1])
print(summaryMatrix[0][0], "|",summaryMatrix[0][1])
print(summaryMatrix[1][0], "|",summaryMatrix[1][1])
print("precision = ",precision)
print("negative predictive value = ",negativePredictiveValue)
print("sensitivity = ",sensitivity)
print("specificity = ",specificity)
print("recall = ",recall)
print("F - measure = ",FMeasure)
print("accuracy = ",accuracy)
    