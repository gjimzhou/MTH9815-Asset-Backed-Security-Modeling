# test.py

"""
Test Functions
Author: gjimzhou
"""

import csv
import multiprocessing as mp
from Waterfall.waterfall import *


def createLoanPool(fileName):
    loanPool = LoanPool()
    with open(fileName, 'r') as file:
        reader = csv.reader(file, delimiter=',')
        next(reader)

        for row in reader:
            loanType, notional, rate, term, assetType, initialValue, depreciateRate = row[1:]
            asset = createAsset(assetType, float(initialValue), float(depreciateRate))
            loan = createLoan(loanType, float(notional), float(rate), float(term), asset)
            loanPool.addLoan(loan)

    return loanPool


def createLoan(loanType, notional, rate, term, asset):
    dictionary = {'Loan': Loan, 'Fixed Rate Loan': FixedRateLoan, 'Variable Rate Loan': VariableRateLoan,
                  'Auto Loan': AutoLoan, 'Fixed Mortgage': FixedMortgage, 'Variable Mortgage': VariableMortgage}
    loanName = dictionary[loanType]
    loan = loanName(notional, rate, term, asset)
    return loan


def createAsset(assetType, initialValue, depreciateRate):
    dictionary = {'Asset': Asset, 'Car': Car, 'Civic': Civic, 'Lexus': Lexus, 'Lamborghini': Lamborghini,
                  'House': House, 'Primary Home': PrimaryHome, 'Vacation Home': VacationHome}
    assetName = dictionary[assetType]
    asset = assetName(initialValue, depreciateRate)
    return asset


def createStructuredSecurity(fileName, loanPool, mode):
    structuredSecurity = StructuredSecurity(loanPool.totalPrincipal(), mode)
    with open(fileName, 'r') as file:
        reader = csv.reader(file, delimiter=',')
        next(reader)

        for row in reader:
            trancheType, percent, rate, subordination, coefficient = row[1:]
            structuredSecurity.addTranche(float(percent), float(rate), subordination, float(coefficient))

    return structuredSecurity


def writeAssets(assets):
    with open('Data/assets.csv', 'w') as file:
        writer = csv.writer(file, delimiter=',')
        header = ['Period', 'Total Interest Due', 'Total Principal Due', 'Total Notional Balance']
        writer.writerow(header)
        writer.writerows(assets)


def writeLiabilities(liabilities):
    with open('Data/liabilities.csv', 'w') as file:
        writer = csv.writer(file, delimiter=',')
        header = ['Period', 'Total Interest Due', 'Total Interest Paid', 'Total Interest Shortfall', 'Principal Paid',
                  'Total Notional Balance']
        writer.writerow(header)
        writer.writerows(liabilities)


def testWaterfall(loanFileName, trancheFileName, mode, simulationNumber, tolerance):
    loanPool = createLoanPool(loanFileName)
    structuredSecurity = createStructuredSecurity(trancheFileName, loanPool, mode)

    print("Now running doWaterfall...")
    assets, liabilities, metrics = doWaterfall(loanPool, structuredSecurity)
    writeAssets(assets)
    writeLiabilities(liabilities)
    print(metrics)

    print("Now running simulateWaterfall...")
    averageDirrs, averageAls, averageDirrRatings = simulateWaterfall(loanPool, structuredSecurity, simulationNumber)
    print(averageDirrs, averageAls, averageDirrRatings)

    print("Now running runMonteCarlo...")
    oldTrancheRates, averageDirrs, averageAls, averageDirrRatings = runMonteCarlo(loanPool, structuredSecurity,
                                                                                  simulationNumber, tolerance)
    print(oldTrancheRates, averageDirrs, averageAls, averageDirrRatings)
