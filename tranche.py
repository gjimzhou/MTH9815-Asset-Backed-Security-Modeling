# tranche.py

"""
Tranche Classes
Author: gjimzhou
"""


class Tranche(object):
    def __init__(self, notional, rate, subordination):
        self._notional = notional
        self._rate = rate
        self._subordination = subordination

    @property
    def notional(self):
        return self._notional

    @property
    def rate(self):
        return self._rate

    @property
    def subordination(self):
        return self._subordination


class StandardTranche(Tranche):
    def __init__(self, notional, rate, subordination):
        super().__init__(notional, rate, subordination)
        self._timePeriod = 0
        self._principalPayments = []
        self._interestPayments = []
        self._interestShortfalls = []
        self._ifPaidPrincipal = 0
        self._ifPaidInterest = 0

    @property
    def timePeriod(self):
        return self._timePeriod

    def increaseTimePeriod(self):
        if self._ifPaidPrincipal == 0:
            self._principalPayments.append(0)
        if self._ifPaidInterest == 0:
            self._interestPayments.append(0)
            self._interestShortfalls.append(self.interestDue())
        self._timePeriod += 1
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
        self._timePeriod = 0
        self._principalPayments = []
        self._interestPayments = []
        self._interestShortfalls = []
        self._ifPaidPrincipal = 0
        self._ifPaidInterest = 0
