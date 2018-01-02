# loan.py

"""
Loan Classes
Author: gjimzhou
"""

from Loan.loanbase import *


class FixedRateLoan(Loan):
    def __init__(self, notional, rate, term):
        super().__init__(notional, rate, term)


class VariableRateLoan(Loan):
    def __init__(self, notional, rateDictionary, term):
        super().__init__(notional, None, term)
        self._rateDictionary = rateDictionary

    @property
    def rateDictionary(self):
        return self._rateDictionary

    @rateDictionary.setter
    def rateDictionary(self, rateDictionary):
        self._rateDictionary = rateDictionary

    def getRate(self, period):
        return self._rateDictionary[period]

    def setRate(self, period, rate):
        self._rateDictionary[period] = rate

    def monthlyPayment(self, period):
        notional = self._notional
        rate = self.monthlyRate(self._rateDictionary[period])
        term = self._term
        return self.calculateMonthlyPayment(notional, rate, term, period)

    def interestDue(self, period):
        rate = self.monthlyRate(self._rateDictionary[period])
        balance = self.balance(period)
        interestDue = balance * rate
        return interestDue

    def balance(self, period):
        notional = self._notional
        rate = self.monthlyRate(self._rateDictionary[period])
        term = self._term
        balance = self.calculateBalance(notional, rate, term, period)
        return balance


class AutoLoan(FixedRateLoan):
    def __init__(self, notional, rate, term):
        super().__init__(notional, rate, term)
