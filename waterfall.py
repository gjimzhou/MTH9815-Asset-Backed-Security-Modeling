# waterfall.py

"""
Waterfall Methods
Author: gjimzhou
"""

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
        totalPayment = loanPool.totalDue(period)[-1]
        structuredSecurity.makePayments(totalPayment)
        loanPoolWaterfall[period] = loanPool.getWaterfall()
        structuredSecurityWaterfall[period] = structuredSecurity.getWaterfall()
        period += 1
        structuredSecurity.increaseTimePeriods()

    metrics = structuredSecurity.getMetrics()

    return [loanPoolWaterfall, structuredSecurityWaterfall, metrics]
