# tranche.py

"""
Tranche Classes
Author: gjimzhou
"""

import numpy as np


class Tranche(object):
    def __init__(self, notional, rate, subordination, coefficient):
        self._notional = notional
        self._rate = rate
        self._subordination = subordination
        self._coefficient = coefficient

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

    @property
    def coefficient(self):
        return self._coefficient

    @coefficient.setter
    def coefficient(self, coefficient):
        self._coefficient = coefficient

    def irr(self):
        pass

    def dirr(self):
        dirr = self._rate - self.irr()
        return dirr

    def al(self):
        pass

    def metrics(self):
        metrics = [self.irr(), self.dirr(), self.al(), self.dirrRating(self.dirr())]
        return metrics

    @staticmethod
    def monthlyRate(annualRate):
        monthlyRate = annualRate / 12
        return monthlyRate

    @staticmethod
    def annualRate(monthlyRate):
        annualRate = monthlyRate * 12
        return annualRate

    @staticmethod
    def dirrRating(dirr):
        dirrs = [0.06, 0.67, 1.3, 2.7, 5.2, 8.9, 13, 19, 27, 46, 72, 106, 143, 183, 231, 311, 2500, 10000]
        ratings = ['Aaa', 'Aa1', 'Aa2', 'Aa3', 'A1', 'A2', 'A3', 'Baa1', 'Baa2', 'Baa3', 'Ba1', 'Ba2', 'Ba3', 'B1',
                   'B2', 'B3', 'Caa', 'Ca']
        index = sum([(dirr * 10000 > d) for d in dirrs])
        rating = ratings[index]
        return rating


class StandardTranche(Tranche):
    def __init__(self, notional, rate, subordination, coefficient):
        super().__init__(notional, rate, subordination, coefficient)
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
        if self._ifPaidPrincipal == 1:
            raise Exception("Already made principal payment for this time period!")
        #elif self.notionalBalance() == 0:
        #    raise Exception("Notional balance is zero!")
        else:
            self._principalPayments.append(principalPayment)
            self._ifPaidPrincipal = 1

    def makeInterestPayment(self, interestPayment):
        interestDue = self.interestDue()
        if self._ifPaidInterest == 1:
            raise Exception("Already made interest payment for this time period!")
        #elif interestDue == 0:
        #    raise Exception("Interest due is zero!")
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
        rate = self.monthlyRate(self._rate)
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
        interestDue = (self._period != 0) * (notionalBalance * rate - interestPayment)
        return interestDue

    def trancheInfo(self):
        interestDue = self.interestDue()
        interestPaid = 0
        interestShortfall = 0
        principalPaid = 0
        notionalBalance = self.notionalBalance()
        if self._ifPaidInterest == 1:
            interestPaid = self._interestPayments[-1]
            interestShortfall = self._interestShortfalls[-1]
        else:
            interestShortfall = interestDue
        if self._ifPaidPrincipal == 1:
            principalPaid = self._principalPayments[-1]
        trancheInfo = [interestDue, interestPaid, interestShortfall, principalPaid, notionalBalance]
        return trancheInfo

    def reset(self):
        self._period = 0
        self._principalPayments = []
        self._interestPayments = []
        self._interestShortfalls = []
        self._notionalBalances = []
        self._ifPaidPrincipal = 0
        self._ifPaidInterest = 0

    def irr(self):
        cashFlow = [-self._notional]
        for i in range(1, self._period):
            totalPayment = self._principalPayments[i] + self._interestPayments[i]
            cashFlow.append(totalPayment)
        return np.irr(cashFlow) * 12

    def al(self):
        al = np.nan
        if self.notionalBalance() == 0:
            periods = list(range(self._period))
            al = np.dot(periods, self._notionalBalances) / self._notional
        return al
