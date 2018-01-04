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
        loanPool.reset()
        structuredSecurity.reset()
        metrics = np.array(doWaterfall(loanPool, structuredSecurity)[-1]).T
        dirrs.append(metrics[1])
        als.append(metrics[2])

    averageDirrs = np.mean(dirrs, axis=0)
    averageAls = np.nanmean(als, axis=0)
    return [averageDirrs, averageAls]


def runMonteCarlo(loanPool, structuredSecurity, simulationNumber, tolerance):
    difference = tolerance * 2
    notionals = structuredSecurity.getNotionals()
    oldTrancheRates = structuredSecurity.getRates()
    coefficients = structuredSecurity.getCoefficients()
    averageDirrs = None
    averageAls = None

    while(difference > tolerance):
        averageDirrs, averageAls = simulateWaterfall(loanPool, structuredSecurity, simulationNumber)
        yieldRates = [calculateYield(d, a) for d, a in zip(averageDirrs, averageAls)]
        newTrancheRates = [calculateNewTrancheRate(y, o, c) for y, o, c in
                           zip(yieldRates, oldTrancheRates, coefficients)]
        difference = calculateDifference(notionals, oldTrancheRates, newTrancheRates)
        oldTrancheRates = newTrancheRates

    return [averageDirrs, averageAls]


def calculateYield(dirr, al):
    yieldRate = ((7 / (1 + 0.08 * np.exp(-0.19 * al / 12))) + 0.019 * np.sqrt(al / 12 * dirr * 100)) / 100
    return yieldRate


def calculateNewTrancheRate(yieldRate, oldTrancheRate, coefficient):
    newTrancheRate = oldTrancheRate + coefficient * (yieldRate - oldTrancheRate)
    return newTrancheRate


def calculateDifference(notionals, oldTrancheRates, newTrancheRates):
    errors = [np.absolute((o - n) / o) for o, n in zip(oldTrancheRates, newTrancheRates)]
    difference = np.average(errors, weights=notionals)
    return difference
