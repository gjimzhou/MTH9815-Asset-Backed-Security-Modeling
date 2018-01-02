# autoloan.py

"""
AutoLoan Classes
Author: gjimzhou
"""

from Loan.loan import *
from Asset.car import *


class AutoLoan(FixedRateLoan):
    def __init__(self, notional, rate, term, car):
        super().__init__(notional, rate, term, car)
        if isinstance(car, Car):
            self._car = car
        else:
            raise Exception("This is not a car!")

    def pmi(self, period):
        notional = self._notional
        rate = self.monthlyRate(self._rate)
        term = self._term
        loanValue = Loan.calculateBalance(notional, rate, term, period)
        assetValue = self._car.currentValue(period)
        ltv = loanValue / assetValue
        pmi = (ltv > 0.8) * 0.000075 * notional
        return pmi

    def monthlyPayment(self, period):
        initialPayment = super().monthlyPayment(period)
        adjustment = self.pmi(period)
        monthlyPayment = initialPayment + adjustment
        return monthlyPayment

    def principalDue(self, period):
        initialPayment = super().principalDue(period)
        adjustment = self.pmi(period)
        principalDue = initialPayment + adjustment
        return principalDue
