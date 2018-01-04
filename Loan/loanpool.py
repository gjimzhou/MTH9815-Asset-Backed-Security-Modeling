# loanpool.py

"""
LoanPool Classes
Author: gjimzhou
"""

from Loan.mortgage import *
from Loan.autoloan import *


class LoanPool(object):
    def __init__(self):
        self._loans = []

    def addLoan(self, loan):
        self._loans.append(loan)

    def totalPrincipal(self):
        notionals = [l.notional for l in self._loans]
        totalPrincipal = sum(notionals)
        return totalPrincipal

    def totalBalance(self, period):
        balances = [l.balance(period) for l in self._loans]
        totalBalance = sum(balances)
        return totalBalance

    def totalDue(self, period):
        principalDues = [l.principalDue(period) for l in self._loans]
        interestDues = [l.interestDue(period) for l in self._loans]
        totalPrincipalDue = sum(principalDues)
        totalInterestDue = sum(interestDues)
        totalDue = totalPrincipalDue + totalInterestDue
        return [totalPrincipalDue, totalInterestDue, totalDue]

    def activeLoan(self, period):
        activeLoans = [(l.balance(period) > 0) for l in self._loans]
        activeLoan = sum(activeLoans)
        return activeLoan

    def checkDefaults(self, period):
        range = [10, 60, 120, 180, 210, 360]
        probabilities = [0.0005, 0.001, 0.002, 0.004, 0.002, 0.001]
        index = sum([(period > r) for r in range])
        numbers = np.random.randint(0, 1 / probabilities[index], len(self._loans))
        recoveryValues = [l.checkDefault(period, n) for l, n in zip(self._loans, numbers)]
        recoveryValue = sum(recoveryValues)
        return recoveryValue

    def reset(self):
        for l in self._loans:
            l.reset()

    def wam(self):
        terms = [l.term for l in self._loans]
        notionals = [l.notional for l in self._loans]
        wam = np.dot(terms, notionals) / self.totalPrincipal()
        return wam

    def war(self):
        rates = [l.rate for l in self._loans]
        notionals = [l.notional for l in self._loans]
        war = np.dot(rates, notionals) / self.totalPrincipal()
        return war

    def getWaterfall(self, period):
        waterfalls = [l.loanInfo(period) for l in self._loans]
        waterfall = [period] + list(np.mean(waterfalls, axis=0))
        return waterfall
