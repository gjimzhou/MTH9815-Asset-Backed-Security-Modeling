# structuredsecurity.py

"""
StructuredSecurity Classes
Author: gjimzhou
"""

from Tranche.tranche import *


class StructuredSecurity(object):
    def __init__(self, totalNotional, mode):
        self._totalNotional = totalNotional
        self._mode = mode
        self._reserveAccount = 0
        self._tranches = []

    @property
    def totalNotional(self):
        return self._totalNotional

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, mode):
        self._mode = mode

    @property
    def reserveAccount(self):
        return self._reserveAccount

    def getNotionals(self):
        notionals = [t.notional for t in self._tranches]
        return notionals

    def getRates(self):
        rates = [t.rate for t in self._tranches]
        return rates

    def getCoefficients(self):
        coefficients = [t.coefficient for t in self._tranches]
        return coefficients

    def addTranche(self, percent, rate, subordination):
        tranche = StandardTranche(self._totalNotional * percent, rate, subordination)
        self._tranches.append(tranche)
        self._tranches.sort(key=lambda t: t.subordination(), reverse=True)

    def increaseTimePeriods(self):
        for t in self._tranches:
            t.increaseTimePeriod()

    def makePayments(self, cashAmount):
        cashAmount += self._reserveAccount

        for t in self._tranches:
            interestDue = t.interestDue()
            interestPayment = min(cashAmount, interestDue)
            t.makeInterestPayment(interestPayment)
            cashAmount -= interestPayment

        if self._mode == 'Sequential':
            for t in self._tranches:
                notionalBalance = t.notionalBalance()
                principalPayment = min(cashAmount, notionalBalance)
                t.makePrincipalPayment(principalPayment)
                cashAmount -= principalPayment
        elif self._mode == 'Pro Rata':
            principalPayments = 0
            for t in self._tranches:
                percent = t.notional / self._totalNotional
                notionalBalance = t.notionalBalance()
                principalPayment = min(cashAmount * percent, notionalBalance)
                t.makePrincipalPayment(principalPayment)
                principalPayments += principalPayment
            cashAmount -= principalPayments

        self._reserveAccount += cashAmount

    def reset(self):
        for t in self._tranches:
            t.reset()

    def getWaterfall(self):
        waterfall = [t.trancheInfo() for t in self._tranches]
        return waterfall

    def getMetrics(self):
        metrics = [t.metrics() for t in self._tranches]
        return metrics
