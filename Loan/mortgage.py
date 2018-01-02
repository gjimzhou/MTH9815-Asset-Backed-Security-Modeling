# mortgage.py

"""
Mortgage Classes
Author: gjimzhou
"""

from Loan.loan import *


class MortgageMixin(Loan):
    def __init__(self, notional, rate, term, asset):
        super().__init__(notional, rate, term)
        self._asset = asset

    def pmi(self, period):
        notional = self._notional
        rate = self.monthlyRate(self._rate)
        term = self._term
        loanValue = Loan.calculateBalance(notional, rate, term, period)
        assetValue = self._asset.currentValue(period)
        ltv = loanValue / assetValue
        pmi = (ltv >= 0.8) * 0.000075 * notional
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


class FixedMortgage(MortgageMixin, FixedRateLoan):
    def __init__(self, notional, rate, term, asset):
        super().__init__(notional, rate, term, asset)


class VariableMortgage(MortgageMixin, VariableRateLoan):
    def __init__(self, notional, rateDictionary, term, asset):
        MortgageMixin.__init__(notional, None, term, asset)
        VariableRateLoan.__init__(notional, rateDictionary, term)
