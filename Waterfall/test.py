# test.py

"""
Test Functions
Author: gjimzhou
"""

import csv
from Waterfall.waterfall import *


def createLoanPool(fileName):
    loanPool = LoanPool()
    with open(fileName) as file:
        reader = csv.reader(file, delimiter=',')
        header = reader.next()

        for row in reader:
            loanType, notional, rate, term, assetType, initialValue, depreciateRate = row[1:]
            asset = createAsset(assetType, initialValue, depreciateRate)
            loan = createLoan(loanType, notional, rate, term, asset)
            loanPool.addLoan(loan)

    return loanPool


def createLoan(loanType, notional, rate, term, asset):
    dictionary = {'Loan': Loan, 'Fixed Rate Loan': FixedRateLoan, 'Variable Rate Loan': VariableRateLoan, 'Auto Loan': AutoLoan, 'Fixed Mortgage': FixedMortgage, 'Variable Mortgage': VariableMortgage}
    loanName = dictionary[loanType]
    loan = loanName(notional, rate, term, asset)


def createAsset(assetType, initialValue, depreciateRate):
    dictionary = {'Asset': Asset, 'Car': Car, 'Civic': Civic, 'Lexus': Lexus, 'Lamborghini': Lamborghini, 'House': House, 'Primary Home': PrimaryHome, 'Vacation Home': VacationHome}
    assetName = dictionary[assetType]
    asset = assetName(initialValue, depreciateRate)
    return asset


def createStructuredSecurity(fileName, loanPool, mode):
    structuredSecurity = StructuredSecurity(loanPool.totalPrincipal(), mode)
    with open(fileName) as file:
        reader = csv.reader(file, delimiter=',')
        header = reader.next()

        for row in reader:
            trancheType, percent, rate, subordination, coefficient = row[1:]
            structuredSecurity.addTranche(percent, rate, subordination, coefficient)

    return structuredSecurity


def testWaterfall():
    pass
