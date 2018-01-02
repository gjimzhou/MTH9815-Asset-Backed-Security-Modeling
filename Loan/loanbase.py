# loanbase.py

"""
Loan Classes
Author: gjimzhou
"""


class Loan(object):
    def __init__(self, notional, rate, term):
        self._notional = notional
        self._rate = rate
        self._term = term

    @property
    def notional(self):
        return self._notional

    @notional.setter
    def notional(self, notional):
        self._notional = notional

    @property
    def rate(self):
        return float(self._rate)

    @rate.setter
    def rate(self, rate):
        self._rate = rate

    @property
    def term(self):
        return float(self._term)

    @term.setter
    def term(self, term):
        self._term = term

    def monthlyPayment(self, period):
        notional = self._notional
        rate = self.monthlyRate(self._rate)
        term = self._term
        return self.calculateMonthlyPayment(notional, rate, term, period)

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
        balance = self.calculateBalance(notional, rate, term, period)
        return balance

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
