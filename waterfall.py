# waterfall.py

"""
Waterfall Methods
Author: gjimzhou
"""

import numpy as np
from Loan.loanpool import *
from Tranche.structuredsecurity import *


def doWaterfall(loanPool, structuredSecurity):
    loanPoolWaterfall = {}
    structuredSecurityWaterfall = {}
    period = 0
    loanPoolWaterfall[period] = loanPool.getWaterfall()
    structuredSecurityWaterfall[period] = structuredSecurity.getWaterfall()
    period += 1
    structuredSecurity.increaseTimePeriods()

    while loanPool.activeLoan(period):
        recoveryValue = loanPool.checkDefaults(period)
        normalPayment = loanPool.totalDue(period)[-1]
        totalPayment = normalPayment + recoveryValue
        structuredSecurity.makePayments(totalPayment)
        loanPoolWaterfall[period] = loanPool.getWaterfall()
        structuredSecurityWaterfall[period] = structuredSecurity.getWaterfall()
        period += 1
        structuredSecurity.increaseTimePeriods()

    metrics = structuredSecurity.getMetrics()

    return [loanPoolWaterfall, structuredSecurityWaterfall, metrics]


def simulateWaterfall(loanPool, structuredSecurity, simulationNumber):
    for i in range(simulationNumber):
        loanPool.reset()
        structuredSecurity.reset()


def runMonte():
    pass


def calculateYield(dirr, al):
    yieldRate = ((7 / (1 + 0.08 * np.exp(-0.19 * al / 12))) + 0.019 * np.sqrt(al / 12 * dirr * 100)) / 100
    return yieldRate
