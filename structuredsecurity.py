# structuredsecurity.py

"""
StructuredSecurity Classes
Author: gjimzhou
"""

from tranche import *


class StructuredSecurity(object):
    def __init__(self, totalNotional, mode):
        self._totalNotional = totalNotional
        self._mode = mode
        self._tranches = []

    @property
    def totalNotional(self):
        return self._totalNotional

    def addTranche(self, percent, rate, subordination):
        self._tranches.append(StandardTranche(self._totalNotional * percent, rate, subordination))
        self._tranches.sort(key=lambda t: t.subordination(), reverse=True)

    def increaseTimePeriods(self):
        for t in self._tranches:
            t.increaseTimePeriod()

    def makePayments(self, cashAmount):
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
            for t in self._tranches:
                percent = t.notional() / self._totalNotional
                principalPayment = cashAmount * percent
                t.makePrincipalPayment(principalPayment)
