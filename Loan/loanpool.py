# loanpool.py

"""
LoanPool Classes
Author: gjimzhou
"""

import numpy as np
from Loan.mortgage import *
from Loan.autoloan import *


class LoanPool(object):
    def __init__(self):
        self._loans = []

    def addLoan(self, loan):
        self._loans.append(loan)

    def totalPrincipal(self):
        totalPrincipal = 0
        for l in self._loans:
            totalPrincipal += l.notional
        return totalPrincipal

    def totalBalance(self, period):
        totalBalance = 0
        for l in self._loans:
            totalBalance += l.balance(period)
        return totalBalance

    def totalDue(self, period):
        totalPrincipalDue = 0
        totalInterestDue = 0
        for l in self._loans:
            totalPrincipalDue += l.principalDue(period)
            totalInterestDue += l.interestDue(period)
        totalDue = totalPrincipalDue + totalInterestDue
        return [totalPrincipalDue, totalInterestDue, totalDue]

    def activeLoan(self, period):
        activeLoan = 0
        for l in self._loans:
            activeLoan += (l.balance(period) > 0)
        return activeLoan

    def checkDefaults(self, period):
        range = [10, 60, 120, 180, 210, 360]
        probabilities = [0.0005, 0.001, 0.002, 0.004, 0.002, 0.001]
        index = sum([(period > r) for r in range])
        numbers = np.random.uniform(0, 1 / probabilities[index], len(self._loans))

    def wam(self):
        wam = 0
        for l in self._loans:
            wam += l.term * l.notional
        wam /= self.totalPrincipal()
        return wam

    def war(self):
        war = 0
        for l in self._loans:
            war += l.rate * l.notional
        war /= self.totalPrincipal()
        return war

    def getWaterfall(self, period):
        waterfall = [l.loanInfo(period) for l in self._loans]
        return waterfall
