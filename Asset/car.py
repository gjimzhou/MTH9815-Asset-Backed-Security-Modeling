# car.py

"""
Car Classes
Author: gjimzhou
"""

from Asset.asset import *


class Car(Asset):
    def __init__(self, initialValue, depreciateRate):
        super().__init__(initialValue, depreciateRate)

    @property
    def depreciateRate(self):
        return self._depreciateRate


class Civic(Car):
    def __init__(self, initialValue, depreciateRate):
        super().__init__(initialValue, depreciateRate)


class Lexus(Car):
    def __init__(self, initialValue, depreciateRate):
        super().__init__(initialValue, depreciateRate)


class Lamborghini(Car):
    def __init__(self, initialValue, depreciateRate):
        super().__init__(initialValue, depreciateRate)
