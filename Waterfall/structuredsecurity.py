# structuredsecurity.py

"""
StructuredSecurity Classes
Author: gjimzhou
"""

from Waterfall.tranche import *


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

    def addTranche(self, percent, rate, subordination):
        self._tranches.append(StandardTranche(self._totalNotional * percent, rate, subordination))
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
                percent = t.notional() / self._totalNotional
                notionalBalance = t.notionalBalance()
                principalPayment = min(cashAmount * percent, notionalBalance)
                t.makePrincipalPayment(principalPayment)
                principalPayments += principalPayment
            cashAmount -= principalPayments

        self._reserveAccount += cashAmount

    def getWaterfall(self):
        waterfall = []

        for t in self._tranches:
            interestDue = t.interestDue()
            interestPaid = 0
            interestShortfall = 0
            principalPaid = 0
            notionalBalance = t.notionalBalance()
            if t.ifPaidInterest() == 1:
                interestPaid = t.interestPayments()[-1]
                interestShortfall = t.interestShortfall()[-1]
            else:
                interestShortfall = interestDue
            if t.ifPaidPrincipal() == 1:
                principalPaid = t.principalPayments()[-1]
            waterfall.append([interestDue, interestPaid, interestShortfall, principalPaid, notionalBalance])

        return waterfall
