# structuredsecurity.py

"""
StructuredSecurity Classes
Author: gjimzhou
"""

from tranche import *


class StructuredSecurity(object):
    def __init__(self, totalNotional):
        self._totalNotional = totalNotional
        self._tranches = []

    @property
    def totalNotional(self):
        return self._totalNotional

    def addTranche(self, notional, rate, subordination):
        self._tranches.append(StandardTranche(notional, rate, subordination))
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
