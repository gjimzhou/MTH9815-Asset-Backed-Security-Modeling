# asset.py

"""
Asset Classes
Author: gjimzhou
"""


class Asset(object):
    def __init__(self, initialValue, depreciateRate):
        self._initialValue = initialValue
        self._depreciateRate = depreciateRate

    @property
    def initialValue(self):
        return self._initialValue

    @initialValue.setter
    def initialValue(self, initialValue):
        self._initialValue = initialValue

    @property
    def depreciateRate(self):
        raise NotImplementedError()

    @depreciateRate.setter
    def depreciateRate(self, depreciateRate):
        self._depreciateRate = depreciateRate

    def currentValue(self, period):
        depreciateRate = self.monthlyDepreciateRate(self._depreciateRate)
        totalDepreciation = (1 - depreciateRate) ** period
        currentValue = self._initialValue * totalDepreciation
        return currentValue

    def recoveryValue(self, period):
        pass

    @staticmethod
    def monthlyDepreciateRate(annualDepreciateRate):
        monthlyDepreciateRate = annualDepreciateRate / 12
        return monthlyDepreciateRate

    @staticmethod
    def annualDepreciateRate(monthlyDepreciateRate):
        annualDepreciateRate = monthlyDepreciateRate * 12
        return annualDepreciateRate
