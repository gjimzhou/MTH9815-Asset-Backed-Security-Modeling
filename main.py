# main.py

"""
Main Function
Author: gjimzhou
"""

from waterfall import *

c = Lamborghini(100, 0.1)
h = PrimaryHome(200, 0.2)
a = AutoLoan(100, 0.05, 5, c)
m = FixedMortgage(200, 0.05, 10, h)
