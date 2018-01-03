# mortgage.py

"""
Mortgage Classes
Author: gjimzhou
"""

from Loan.loan import *
from Asset.house import *


class MortgageMixin(Loan):
    def __init__(self, notional, rate, term, house):
        if isinstance(house, House):
            super().__init__(notional, rate, term, house)
            self._house = self._asset
        else:
            raise Exception("This is not a house!")

    def pmi(self, period):
        notional = self._notional
        loanValue = self.balance(period)
        assetValue = self._house.currentValue(period)
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


class FixedMortgage(MortgageMixin, FixedRateLoan):
    def __init__(self, notional, rate, term, house):
        super().__init__(notional, rate, term, house)


class VariableMortgage(MortgageMixin, VariableRateLoan):
    def __init__(self, notional, rateDictionary, term, house):
        MortgageMixin.__init__(notional, None, term, house)
        VariableRateLoan.__init__(notional, rateDictionary, term)
