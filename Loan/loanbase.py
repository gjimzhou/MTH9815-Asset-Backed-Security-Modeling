# loanbase.py

"""
Loan Classes
Author: gjimzhou
"""

from Asset.asset import *


class Loan(object):
    def __init__(self, notional, rate, term, asset):
        self._notional = notional
        self._rate = rate
        self._term = term
        if isinstance(asset, Asset):
            self._asset = asset
        else:
            raise Exception("This is not an asset!")
        self._ifDefault = 0

    @property
    def notional(self):
        return self._notional

    @notional.setter
    def notional(self, notional):
        self._notional = notional

    @property
    def rate(self):
        return self._rate

    @rate.setter
    def rate(self, rate):
        self._rate = rate

    @property
    def term(self):
        return self._term

    @term.setter
    def term(self, term):
        self._term = term

    def monthlyPayment(self, period):
        notional = self._notional
        rate = self.monthlyRate(self._rate)
        term = self._term
        default = self._ifDefault
        return (default == 0) * self.calculateMonthlyPayment(notional, rate, term, period)

    def totalPayment(self):
        totalPayment = 0
        term = self._term
        for t in range(1, term + 1):
            totalPayment += self.monthlyPayment(t)
        return totalPayment

    def totalInterest(self):
        totalInterest = self.totalPayment() - self._notional
        return totalInterest

    def interestDue(self, period):
        rate = self.monthlyRate(self._rate)
        balance = self.balance(period)
        interestDue = balance * rate
        return interestDue

    def principalDue(self, period):
        monthlyPayment = self.monthlyPayment(period)
        interestDue = self.interestDue(period)
        principalDue = monthlyPayment - interestDue
        return principalDue

    def balance(self, period):
        notional = self._notional
        rate = self.monthlyRate(self._rate)
        term = self._term
        default = self._ifDefault
        balance = (default == 0) * self.calculateBalance(notional, rate, term, period)
        return balance

    def loanInfo(self, period):
        interestDue = self.interestDue(period)
        principalDue = self.principalDue(period)
        notionalBalance = self.balance(period)
        loanInfo = [interestDue, principalDue, notionalBalance]
        return loanInfo

    def recoveryValue(self, period):
        recoveryValue = self._asset.currentValue(period) * 0.6
        return recoveryValue

    def equity(self, period):
        loanValue = self.balance(period)
        assetValue = self._asset.currentValue(period)
        equity = assetValue - loanValue
        return equity

    def checkDefault(self, period, number):
        recoveryValue = 0
        if number == 0:
            self._ifDefault = 1
            recoveryValue += self._asset.recoveryValue(period)
        return recoveryValue

    @classmethod
    def calculateMonthlyPayment(cls, notional, rate, term, period):
        monthlyPayment = rate * notional / (1 - (1 + rate) ** (-term))
        return monthlyPayment

    @classmethod
    def calculateBalance(cls, notional, rate, term, period):
        balance = notional * (1 + rate) ** period
        balance -= cls.calculateMonthlyPayment(notional, rate, term, period) * ((1 + rate) ** period - 1) / rate
        balance = max(balance, 0)
        return balance

    @staticmethod
    def monthlyRate(annualRate):
        monthlyRate = annualRate / 12
        return monthlyRate

    @staticmethod
    def annualRate(monthlyRate):
        annualRate = monthlyRate * 12
        return annualRate
