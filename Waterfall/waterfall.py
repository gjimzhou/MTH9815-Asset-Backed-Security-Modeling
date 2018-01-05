# waterfall.py

"""
Waterfall Methods
Author: gjimzhou
"""

from Loan.loanpool import *
from Tranche.structuredsecurity import *


def doWaterfall(loanPool, structuredSecurity):
    period = 0
    loanPoolWaterfall = [loanPool.getWaterfall(period)]
    structuredSecurityWaterfall = [structuredSecurity.getWaterfall(period)]
    period += 1
    structuredSecurity.increaseTimePeriods()

    while loanPool.activeLoan(period):
        recoveryValue = loanPool.checkDefaults(period)
        normalPayment = loanPool.totalDue(period)[-1]
        totalPayment = normalPayment + recoveryValue
        structuredSecurity.makePayments(totalPayment)
        loanPoolWaterfall.append(loanPool.getWaterfall(period))
        structuredSecurityWaterfall.append(structuredSecurity.getWaterfall(period))
        period += 1
        structuredSecurity.increaseTimePeriods()
    metrics = structuredSecurity.getMetrics()
    return [loanPoolWaterfall, structuredSecurityWaterfall, metrics]


def simulateWaterfall(loanPool, structuredSecurity, simulationNumber):
    dirrs = []
    als = []

    for i in range(simulationNumber):
        if i % 200 == 0:
            print('Loop Number: ', i)
        loanPool.reset()
        structuredSecurity.reset()
        metrics = np.array(doWaterfall(loanPool, structuredSecurity)[-1]).T
        metrics = np.array(metrics[:-1], float)
        dirrs.append(metrics[1])
        als.append(metrics[2])

    averageDirrs = np.mean(dirrs, axis=0)
    averageAls = np.nanmean(als, axis=0)
    averageDirrRatings = [dirrRating(a) for a in averageDirrs]
    return [averageDirrs, averageAls, averageDirrRatings]


def runMonteCarlo(loanPool, structuredSecurity, simulationNumber, tolerance):
    iterationNumber = 0
    difference = tolerance * 2
    notionals = structuredSecurity.getNotionals()
    oldTrancheRates = structuredSecurity.getRates()
    coefficients = structuredSecurity.getCoefficients()
    averageDirrs = None
    averageAls = None
    averageDirrRatings = None

    while(difference > tolerance):
        print('Iteration Number: ', iterationNumber)
        averageDirrs, averageAls, averageDirrRatings = simulateWaterfall(loanPool, structuredSecurity, simulationNumber)
        yieldRates = [calculateYield(d, a) for d, a in zip(averageDirrs, averageAls)]
        newTrancheRates = [calculateNewTrancheRate(y, o, c) for y, o, c in
                           zip(yieldRates, oldTrancheRates, coefficients)]
        difference = calculateDifference(notionals, oldTrancheRates, newTrancheRates)
        oldTrancheRates = newTrancheRates
        iterationNumber += 1

    return [oldTrancheRates, averageDirrs, averageAls, averageDirrRatings]


def dirrRating(dirr):
    dirrs = [0.06, 0.67, 1.3, 2.7, 5.2, 8.9, 13, 19, 27, 46, 72, 106, 143, 183, 231, 311, 2500, 10000]
    ratings = ['Aaa', 'Aa1', 'Aa2', 'Aa3', 'A1', 'A2', 'A3', 'Baa1', 'Baa2', 'Baa3', 'Ba1', 'Ba2', 'Ba3', 'B1', 'B2',
               'B3', 'Caa', 'Ca']
    index = sum([(dirr * 10000 > d) for d in dirrs])
    rating = ratings[index]
    return rating


def calculateYield(dirr, al):
    dirr = max(dirr, 0)
    al = max(al, 0)
    yieldRate = ((7 / (1 + 0.08 * np.exp(-0.19 * al / 12))) + 0.019 * np.sqrt(al / 12 * dirr * 100)) / 100
    return yieldRate


def calculateNewTrancheRate(yieldRate, oldTrancheRate, coefficient):
    newTrancheRate = oldTrancheRate + coefficient * (yieldRate - oldTrancheRate)
    return newTrancheRate


def calculateDifference(notionals, oldTrancheRates, newTrancheRates):
    errors = [np.absolute((o - n) / o) for o, n in zip(oldTrancheRates, newTrancheRates)]
    difference = np.average(errors, weights=notionals)
    return difference
