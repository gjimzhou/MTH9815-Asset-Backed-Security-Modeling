# main.py

"""
Main Function
Author: gjimzhou
"""

from Waterfall.test import *


loanFileName = 'Data/loans.csv'
trancheFileName = 'Data/tranches.csv'
mode = 'Sequential'
simulationNumber = 2000
tolerance = 0.005
testWaterfall(loanFileName, trancheFileName, mode, simulationNumber, tolerance)
