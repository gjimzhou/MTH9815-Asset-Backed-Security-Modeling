# tranche.py

"""
Tranche Classes
Author: gjimzhou
"""

import numpy as np


class Tranche(object):
    def __init__(self, notional, rate, subordination):
        self._notional = notional
        self._rate = rate
        self._subordination = subordination

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
    def subordination(self):
        return self._subordination

    @subordination.setter
    def subordination(self, subordination):
        self._subordination = subordination

    def irr(self):
        pass

    def dirr(self):
        dirr = self._rate - self.irr()
        return dirr

    def al(self):
        pass


class StandardTranche(Tranche):
    def __init__(self, notional, rate, subordination):
        super().__init__(notional, rate, subordination)
        self._period = 0
        self._principalPayments = []
        self._interestPayments = []
        self._interestShortfalls = []
        self._notionalBalances = []
        self._ifPaidPrincipal = 0
        self._ifPaidInterest = 0

    @property
    def period(self):
        return self._period

    @property
    def principalPayments(self):
        return self._principalPayments

    @property
    def interestPayments(self):
        return self._interestPayments

    @property
    def interestShortfalls(self):
        return self._interestShortfalls

    @property
    def ifPaidPrincipal(self):
        return self._ifPaidPrincipal

    @property
    def ifPaidInterest(self):
        return self._ifPaidInterest

    def increaseTimePeriod(self):
        if self._ifPaidPrincipal == 0:
            self._principalPayments.append(0)
        if self._ifPaidInterest == 0:
            self._interestPayments.append(0)
            self._interestShortfalls.append(self.interestDue())
        self._notionalBalances.append(self.notionalBalance())
        self._period += 1
        self._ifPaidPrincipal = 0
        self._ifPaidInterest = 0

    def makePrincipalPayment(self, principalPayment):
        notionalBalance = self.notionalBalance()
        if self._ifPaidPrincipal == 1:
            raise Exception("Already made principal payment for this time period!")
        elif notionalBalance == 0:
            raise Exception("Notional balance is zero!")
        else:
            self._principalPayments.append(principalPayment)
            self._ifPaidPrincipal = 1

    def makeInterestPayment(self, interestPayment):
        interestDue = self.interestDue()
        if self._ifPaidInterest == 1:
            raise Exception("Already made interest payment for this time period!")
        elif interestDue == 0:
            raise Exception("Interest due is zero!")
        else:
            self._interestPayments.append(interestPayment)
            self._interestShortfalls.append(interestDue - interestPayment)
            self._ifPaidInterest = 1

    def notionalBalance(self):
        notionalBalance = self._notional
        notionalBalance -= sum(self._principalPayments)
        notionalBalance += sum(self._interestShortfalls)
        return notionalBalance

    def interestDue(self):
        notionalBalance = self.notionalBalance()
        principalPayment = 0
        interestPayment = 0
        interestShortfall = 0
        if self._ifPaidPrincipal == 1:
            principalPayment += self._principalPayments[-1]
        if self._ifPaidInterest == 1:
            interestPayment += self._interestPayments[-1]
            interestShortfall += self._interestShortfalls[-1]
        notionalBalance += principalPayment
        notionalBalance -= interestShortfall
        interestDue = notionalBalance * self._rate
        interestDue -= interestPayment
        return interestDue

    def reset(self):
        self._period = 0
        self._principalPayments = []
        self._interestPayments = []
        self._interestShortfalls = []
        self._ifPaidPrincipal = 0
        self._ifPaidInterest = 0

    def irr(self):
        cashFlow = [self._notional]
        for i in range(1, self._period):
            totalPayment = self._principalPayments[i] + self._interestPayments[i]
            cashFlow.append(totalPayment)
        return np.irr(cashFlow) * 12

    def al(self):
        periods = list(range(self._period))
        al = np.dot(periods, self._notionalBalances) / self._notional
        return al
