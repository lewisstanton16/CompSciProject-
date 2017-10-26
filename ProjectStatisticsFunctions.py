#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 12:13:56 2017

@author: lewisstanton
"""

from __future__ import division
from sympy import *
from sympy.stats import *
from math import *
from scipy import *
from itertools import groupby


sampleScores = [90,80,70,60,50,40,30,30,20,40]
sampleDifficulties = [10,20,35,50,60,75,80,90,95,25]
sampleSize = len(sampleScores)
newSampleScores = [90,90,50,90,90,90,90,90,90,90,200]
newSampleSize = len(newSampleScores)
newSampleMean = CalculateMean(newSampleSize,GetSum(newSampleScores))

#Adding together all the values of the items in an array
def GetSum(sampleScores):
    sumX=0
    for item in sampleScores:
        sumX = sumX+item
            
    return sumX
    
sumScores = GetSum(sampleScores)
sumDifficulties = GetSum(sampleDifficulties)

#Adding together all the values in array squared
def GetSumSquared(sampleScores):
    sumXsquared = 0
    for item in sampleScores:
        sumXsquared = sumXsquared + item**2
        
    return sumXsquared

sumScoressquared = GetSumSquared(sampleScores)
sumDifficultiessquared = GetSumSquared(sampleDifficulties)

#Getting sum of each corresponding value in each array multiplied together
def GetSumXY(sampleScores,sampleDifficulties):
    sumXY = 0
    for i in range(0,len(sampleScores)):
        sumXY = sumXY +(sampleScores[i]*sampleDifficulties[i])
        
    return sumXY

sumScoresDifficulties = GetSumXY(sampleScores,sampleDifficulties)


#Calculates the variance of the numbers in the array
def CalculateVar(sampleSize,sumScores,sumScoressquared):
    varX = sumScoressquared - (((sumScores)**2)/sampleSize)
    return varX

varScores = CalculateVar(sampleSize,sumScores,sumScoressquared)
varDifficulties = CalculateVar(sampleSize,sumDifficulties,sumDifficultiessquared)


#Calculates the variance between two variables
def CalculateVarXY(sampleSize,sumX,sumY,sumXY):
    varXY = sumXY - ((sumX*sumY)/sampleSize)
    return varXY

varScoresDifficulties = CalculateVarXY(sampleSize,sumX,sumDifficulties,sumScoresDifficulties)

#Calculates the mean of the numbers in the array
def CalculateMean(sampleSize,sumX):
    meanX = sumX/sampleSize
    return meanX

meanScores = CalculateMean(sampleSize,sumScores)
meanDifficulties = CalculateMean(sampleSize,sumDifficulties)

#Calculates the standard deviation of the numbers in an array
def CalculateStdDevScores(sampleSize,meanX,sumXsquared):
    stdDev = sqrt((sumXsquared-(sampleSize*(meanX)**2))/(sampleSize-1))
    return stdDev

stdDev = CalculateStdDevScores(sampleSize,meanScores,sumScoressquared)

#Calculates the gradient of the line of best fit
def CalculateGradient(varXY,varX):
    gradient = varXY/varX
    return gradient

gradient = CalculateGradient(varScores,varScores)

#Calculates where the line of best fit will intercept the y axis
def CalculateIntercept(gradient,meanY,meanX):
    intercept = meanY - (gradient*meanX)
    return intercept

intercept = CalculateIntercept(gradient,meanDifficulties,meanScores)


#Creates a Sympy Object of the regression Line
def CreateRegressionLine(gradient,intercept):
    x = Symbol('x')
    y = Symbol('y')
    regressionLine = (gradient*x) + intercept
    return regressionLine

regressionLine = CreateRegressionLine(gradient,intercept)

#Finds the correlation between the scores and the difficulties
def CalculatePMCC(varXY,varX,varY):
    PMCC = varXY/(sqrt(varX*varY))
    return PMCC

PMCC = CalculatePMCC(varScoresDifficulties,varScores,varDifficulties)

def GroupSampleScores(sampleScores):
    group = []

#Tests whether the normal distribution is an accurate model of the grades
def GoodnessOfFitTest(sampleSize,meanX,stdDev,sampleScores):
    print ("Testing a normal Distribution model of mean " + str(meanX) + " and a standard Deviation of " + str(stdDev))
    tempSamplesize = 16
    #Sets up the parameters for the Goodness Of Fit Test
    confidenceInterval = 0.01
    degreesOffreedom = tempSamplesize - 3
    expectedFrequencies = []
    tempSortedarray = [[4,5,10,14,25],[30,37,45,50,55,56],[60,68,75,80,89]]
    ranges = []
    observedFrequencyarray = []
    #Makes an array of how often each range of values is observed in the sample
    for i in range(0,len(tempSortedarray)):
        observedFrequencyarray.append(len(tempSortedarray[i]))
    print (observedFrequencyarray)
    #Makes an array of the ranges that are in each part of the sample
    for i in range(0,len(tempSortedarray)):
        maxInt = max(tempSortedarray[i])
        minInt = min(tempSortedarray[i])
        upperRange = int(math.ceil(maxInt/10)*10)
        lowerRange = int(math.floor(minInt/10)*10)
        ranges.append([])
        ranges[i].append(lowerRange)
        ranges[i].append(upperRange)
    print(ranges)
    #Finds the expected probability based on a normal distribution model
    for i in range(0,len(tempSortedarray)):
        upperBoundprobability = 0.5 * (1+ erf((ranges[i][1]-meanX)/(stdDev*sqrt(2))))
        lowerBoundprobability = 0.5 * (1+ erf((ranges[i][0]-meanX)/(stdDev*sqrt(2))))
        probabilityOfrange = upperBoundprobability-lowerBoundprobability
        expectedFrequencies.append(probabilityOfrange*tempSamplesize)
    print(expectedFrequencies)
    
    sumOfgoodnessOffit = 0
    #Adds together the difference between the observed values and expected values squared divided by the expected values
    for i in range(0,len(observedFrequencyarray)):
        sumOfgoodnessOffit = sumOfgoodnessOffit + ((observedFrequencyarray[i]-expectedFrequencies[i])/expectedFrequencies[i])
    
    #Finds the critical value for which the model will be rejected or approved    
    chiSquared = chi2.isf(confidenceInterval,degreesOffreedom)
    if sumOfgoodnessOffit > chiSquared:
        return False
    else:
        return True    
        
        
    
    
if GoodnessOfFitTest(sampleSize,meanScores,stdDev,sampleScores):
    print("The normal distribution is a suitable model")
else:
    print("The Normal distribution is not a suitable model")



#Test whether the model should be adjusted    
def HypothesisTestForAccuracy(meanSample,stdDev,newSampleSize,newSampleScores,oldMean):
    #Set the parameter for the hypothesis test
    confidenceLevel = 0.05
    #Find the critical values for which the hypothesis should be rejected or approved
    lowerBound = norm.ppf(confidenceLevel,loc=oldMean,scale=stdDev)
    upperBound = -lowerBound
    
    testStatistic = ((meanSample-oldMean)/(stdDev/sqrt(newSampleSize)))

    if testStatistic > upperBound or testStatistic< lowerBound:
        return False
    else:
        return True

    
if HypothesisTestForAccuracy(newSampleMean,stdDev,newSampleSize,newSampleScores,meanScores):
    print("The model is accurate")
else:
    print("The model is not accurate")

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    