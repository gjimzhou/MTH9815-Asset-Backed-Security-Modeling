# house.py

"""
House Classes
Author: gjimzhou
"""

from Asset.asset import *


class House(Asset):
    def __init__(self, initialValue, depreciateRate):
        super().__init__(initialValue, depreciateRate)

    @property
    def depreciateRate(self):
        return self._depreciateRate


class PrimaryHome(House):
    def __init__(self, initialValue, depreciateRate):
        super().__init__(initialValue, depreciateRate)


class VacationHome(House):
    def __init__(self, initialValue, depreciateRate):
        super().__init__(initialValue, depreciateRate)
