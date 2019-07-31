import pandas as pd
import pandas_datareader as pdr
import datetime
import re
import numpy as np

# read in stock codes from an array
def readStockFromList(stockList):

    # Set dates
    start = datetime.datetime(2018, 6, 1)
    end = datetime.datetime(2019, 6, 1)

    all_returns_monthly = []

    # Read data for stock
    for i in stockList:
        try:
            df = pdr.get_data_yahoo(i, start=start, end=end, interval='m')
            all_returns_monthly.append(df['Adj Close'])
            continue
        except (KeyError):
            return []

    return all_returns_monthly

# =======================================
# return an array of the monthly returns, maximum size 10
def readStock():

    # Set dates
    start = datetime.datetime(2018, 6, 1)
    end = datetime.datetime(2019, 6, 1)

    all_returns_monthly = []

    stock_code = raw_input("Stock code name: ")

    counter = 0

    # Read data for stock
    while True:
        try:
            # Uncomment and change to 'W' you want weekly, 'M' for monthly or 'Y' for yearly returns
            if (counter >= 10):
                break

            if (stock_code == 'done'):
                break

            df = pdr.get_data_yahoo(stock_code, start=start, end=end, interval='m')

            # df = pdr.DataReader(stock_code_1, 'yahoo', start, end)
            # df = df.groupby(pd.Grouper(freq='M')).mean()

            all_returns_monthly.append(df['Adj Close'])
            counter = counter + 1
            stock_code = raw_input("Enter a code for the next stock: ")
            continue
        except (KeyError, pdr._utils.RemoteDataError) as e:

            # If invalid, as for a good stock code
            stock_code = raw_input("Enter a valid code for the stock: ")
            continue
        break

    return all_returns_monthly
# =====================================

# returns the risk_free_rate in percentage
def readRiskFree():
    risk_free_string = raw_input("Risk Free Rate (Annual) (in percentage form ex. 5.25%): ")
    while True:
        try:
            # Parse for percentage
            risk_free_rate = float(re.findall(r'(\d+(\.\d+)?%)', risk_free_string)[0][0].rstrip("%")) / 100.0000
        except IndexError:
            # Ask again if not valid
            risk_free_string = raw_input("Please enter a percentage value of the form X.XX%: ")
            continue
        break

    return risk_free_rate
# ======================================

def calcPortfolio(risk_free_rate , all_returns_monthly):
    # risk_free_rate = readRiskFree()
    # all_returns_monthly = readStock()
    counter = len(all_returns_monthly)

    # Get monthly risk free rate
    risk_free_rate_monthly = np.power([risk_free_rate + 1], [1.0 / 12.0])[0] - 1

    returns_monthly = []
    for stock in all_returns_monthly:
        returns_monthly.append(stock.pct_change()[1:])

    average_returns_monthly = []
    variance_monthly = []
    std_monthly = []
    returns_annual = []
    for i in range(0, counter):
        average_returns_monthly.append(returns_monthly[i].mean())
        variance_monthly.append(returns_monthly[i].var())
        std_monthly.append(returns_monthly[i].std())

    for i in range(0, counter):
        returns_annual.append((1 + average_returns_monthly[i]) ** 12 - 1)

    covariances_monthly = []

    for i in range(0, counter):
        variances = []
        for j in range(0, counter):
            variances.append(np.cov(returns_monthly[i].to_numpy(), returns_monthly[j].to_numpy())[0][1])
        covariances_monthly.append(variances)

    covariances_annual = []
    for i in covariances_monthly:
        variances = []
        for j in i:
            variances.append(j * 12)
        covariances_annual.append(variances)

    proportions = [1.0 / float(counter)] * counter
    total = 0.0

    portfolio_return = np.dot(returns_annual, proportions)
    portfolio_risk = 0

    for i in range(0, counter):
        portfolio_risk += covariances_annual[i][i] * proportions[i] ** 2

    for i in range(1, counter):
        for j in range(0, i):
            portfolio_risk += 2 * proportions[i] * proportions[j] * covariances_annual[i][j]

    portfolio_risk = np.sqrt(portfolio_risk)

    portfolioResult = {'ret': portfolio_return, 'risk': portfolio_risk,
                       'stocks': {'returnAnn': returns_annual, 'covAnn': covariances_annual}}

    return portfolioResult
# ==================================================================


# print out the composite stocks & the portfolio stats
def printPortfolio(portfolio):
    returns_annual = portfolio['stocks']['returnAnn']
    covariances_annual = portfolio['stocks']['covAnn']
    portfolio_risk = portfolio['risk']
    portfolio_return = portfolio['ret']

    '''
    for i in range(0, len(returns_annual)):
        print''
        print("Stock {}:").format(i)
        print("\tReturn: {}%").format(returns_annual[i] * 100.00)
        print("\tVariance: {}%").format(covariances_annual[i][i] * 100.00)
        print("\tStandard Deviation: {}%").format(np.sqrt(covariances_annual[i][i] * 100.00))

    print
    '''
    #print("Portfolio Risk: {}%").format(portfolio_risk * 100.00)
    #print("Portfolio Return: {}%").format(portfolio_return * 100.00)
# ================================================

# the function that initiates the process of calculating a custom portfolio
def genEvenPortfolio(stocklist=None, printIf=-1):


    try:
        if not (stocklist is None) :
            all_returns_monthly = readStockFromList(stocklist)
        else :
            all_returns_monthly = readStock()

    #risk_free_rate = readRiskFree()
        risk_free_rate = 0.05

        portfolioResult = calcPortfolio(risk_free_rate, all_returns_monthly)

        if printIf:
            printPortfolio(portfolioResult)

        return portfolioResult
    except:
        return {'ret': 0, 'risk': 1, 'stocks': {'returnAnn': 0.00, 'covAnn': 1}}
