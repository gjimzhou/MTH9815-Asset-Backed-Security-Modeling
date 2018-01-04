# test.py

"""
Test Functions
Author: gjimzhou
"""

import csv
from Waterfall.waterfall import *


def createLoanPool(fileName):
    loanPool = LoanPool()
    with open(fileName, 'rb') as file:
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
    with open(fileName, 'rb') as file:
        reader = csv.reader(file, delimiter=',')
        header = reader.next()

        for row in reader:
            trancheType, percent, rate, subordination, coefficient = row[1:]
            structuredSecurity.addTranche(percent, rate, subordination, coefficient)

    return structuredSecurity


def writeAssets(assets):
    with open('assets.csv', 'wb') as file:
        writer = csv.writer(file, delimiter=',')
        header = ['Total Interest Due', 'Total Principal Due', 'Total Notional Balance']
        writer.writerow(header)
        writer.writerows(assets)


def writeLiabilities(liabilities):
    with open('liabilities.csv', 'wb') as file:
        writer = csv.writer(file, delimiter=',')
        header = ['Total Interest Due', 'Total Interest Paid', 'Total Interest Shortfall', 'Principal Paid', 'Total Notional Balance']
        writer.writerow(header)
        writer.writerows(liabilities)


def testWaterfall(loanFileName, trancheFileName, mode, simulationNumber, tolerance):
    loanPool = createLoanPool(loanFileName)
    structuredSecurity = createStructuredSecurity(trancheFileName, loanPool, mode)

    print("Now running doWaterfall...")
    assets, liabilities, metrics = doWaterfall(loanPool, structuredSecurity)
    writeAssets(assets)
    writeLiabilities(liabilities)

    print("Now running simulateWaterfall...")
    averageDirrs, averageAls = simulateWaterfall(loanPool, structuredSecurity, simulationNumber)
    print(averageDirrs, averageAls)

    print("Now running runMonteCarlo...")
    averageDirrs, averageAls = runMonteCarlo(loanPool, structuredSecurity, simulationNumber, tolerance)
    print(averageDirrs, averageAls)

