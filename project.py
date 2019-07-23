import pandas_datareader as pdr
import pandas as pd
import numpy as np
import re
import datetime

# Set dates
start = datetime.datetime(2018, 6, 1)
end = datetime.datetime(2019, 6, 1)

# Get Stock Codes and Risk Free Rate
stock_1 = []
stock_code_1 = raw_input("Stock code name 1: ")

# Read data for stock 1
while True:
    try:
        df = pdr.DataReader(stock_code_1, 'yahoo', start, end)

        # Uncomment and change if you want weekly, monthly or yearly returns
        df = df.groupby(pd.Grouper(freq='M')).mean()
        stock_1 = df['Adj Close']
    except pdr._utils.RemoteDataError:
        stock_code_1 = raw_input("Enter a valid code for Stock 1: ")
        continue;
    break

# Read data for stock 2
stock_code_2 = raw_input("Stock code name 2: ")
while True:
    try:
        df = pdr.DataReader(stock_code_2, 'yahoo', start, end)

        # Uncomment and change if you want weekly, monthly or yearly returns
        df = df.groupby(pd.Grouper(freq='M')).mean()
        stock_2 = df['Adj Close']
    except pdr._utils.RemoteDataError:
        stock_code_2 = raw_input("Enter a valid code for Stock 2: ")
        continue;
    break

risk_free_string = raw_input("Risk Free Rate (in percentage form ex. 5.25%): ")
risk_free_rate = float(re.findall(r'(\d+(\.\d+)?%)', risk_free_string)[0][0].rstrip("%"))/100.0000

# Calculate returns for both stocks
returns_monthly_1 = []
returns_monthly_2 = []
returns_annual_1 = 0
returns_annual_2 = 0

row = 0
for x in range(len(stock_1) - 1):
    returns_monthly_1.append(stock_1[row+1]/stock_1[row]-1)
    returns_annual_1 = (1 + np.average(returns_monthly_1))**12 - 1
    returns_monthly_2.append(stock_2[row+1]/stock_2[row]-1)
    returns_annual_2 = (1 + np.average(returns_monthly_2))**12 - 1
    row = row + 1

# Calculate statistics for returns
average_return_1 = np.average(returns_monthly_1)
average_return_2 = np.average(returns_monthly_2)

variance_1 = np.var(returns_monthly_1)
variance_2 = np.var(returns_monthly_2)

stdev_1 = np.std(returns_monthly_1)
stdev_2 = np.std(returns_monthly_2)

covariance = np.cov(returns_monthly_1, returns_monthly_2)[0][1]
covariance_annual = covariance * 12
# Min Variance Portfolio

proportion_1 = (variance_2 - covariance)/(variance_1 + variance_2 - 2*covariance)
proportion_2 = (1 - proportion_1)

mvp_return = proportion_1 * average_return_1 + proportion_2 * average_return_2
mvp_risk = np.sqrt(proportion_1**2 * variance_1 + proportion_2**2 * variance_2 + 2 * proportion_1 * proportion_2 * covariance)

print ''
print 'Minimum Variance Portfolio: '
#print '\tMVP proportion ', stock_code_1, ': ', proportion_1 * 10000/100.00, '%'
print('\tMVP proportion {}: {:.3f}%').format(stock_code_1, proportion_1 * 100.00)
#print '\tMVP proportion ', stock_code_2, ': ', proportion_2 * 10000/100.00, '%'
print('\tMVP proportion {}: {:.3f}%').format(stock_code_2, proportion_2 * 100.00)
#print '\tMVP standard deviation: ', mvp_risk * 10000/100.00, '%'
print('\tMVP standard deviation: {:.3f}%').format(mvp_risk * 100.00)
#print '\tMVP expected portfolio return: ', mvp_return * 10000/100.00, '%'
print('\tMVP standard portfolio return: {:.3f}%').format(mvp_return * 100.00)

# Maximize Sharpre Ratio

w_1 = 0.0
w_2 = 1.0

max_r = (w_1 * average_return_1 + w_2 * average_return_2 - risk_free_rate) / np.sqrt(w_1**2 * variance_1 + w_2**2 * variance_2 + 2 * w_1 * w_2 * covariance)
max_w1 = 0.0
max_w2 = 1

for x in range(0, 10000):
    w_1 = w_1 + 0.0001
    w_2 = w_2 - 0.0001
    e_rp = w_1 * average_return_1 + w_2 * average_return_2
    excess_return = e_rp - risk_free_rate
    sharpe_ratio = excess_return / np.sqrt(w_1**2 * variance_1 + w_2**2 * variance_2 + 2 * w_1 * w_2 * covariance)

    if(sharpe_ratio > max_r):
        max_r = sharpe_ratio
        max_w1 = w_1
        max_w2 = w_2

max_return = (max_w1 * average_return_1 + max_w2 * average_return_2)
max_risk = np.sqrt(max_w1 ** 2 * variance_1 + max_w2 ** 2 * variance_2 + 2 * max_w1 * max_w2 * covariance)

print ''
print 'Case 1: '
print '\tGiven-Proportion invested in risk-free asset: 0%'
print '\tGiven-Proportion invested in market portfolio: 100%'
print ('\tMaximum Sharpe ratio: {:.3f}').format(max_r)
#print '\tMarket portfolio proportion ', stock_code_1, ": ", max_w1 * 100, "%"
print ('\tMarket portfolio proportion {}: {:.3f}%').format(stock_code_1, max_w1 * 100.00)
#print '\tMarket portfolio proportion ', stock_code_2, ": ", max_w2 * 100, "%"
print ('\tMarket portfolio proportion {}: {:.3f}%').format(stock_code_2, max_w2 * 100.00)
#print '\tMarket portfolio expected return: ', max_return * 10000/100.00, "%"
print ('\tMarket portfolio expected return: {:.3f}%').format(max_return * 100.00)
#print '\tMarket portfolio standard deviation: ', max_risk * 10000/100.00, "%"
print ('\tMarket portfolio standard deviation: {:.3f}%').format(np.sqrt(max_risk) * 100.00)

print ''
print 'Case 2: '
print '\tGiven-Proportion invested in risk-free asset: 50%'
print '\tGiven-Proportion invested in market portfolio: 50%'
#print '\tPortfolio expected return: ', (0.5 * max_return + 0.5 * risk_free_rate) * 10000/100.00, "%"
print ('\tPortfolio expected return: {:.3f}%').format((0.5 * max_return + 0.5 * risk_free_rate) * 100.00)
#print '\tPortfolio standard deviation: ', (0.5 * np.sqrt(max_risk))* 10000/100.00, "%"
print ('\tPortfolio standard deviation: {:.3f}%').format((0.5 * np.sqrt(max_risk)) * 100.00)

print ''
print 'Case 3: '
print '\tGiven-Proportion invested in risk-free asset: -50%'
print '\tGiven-Proportion invested in market portfolio: 150%'
#print '\tPortfolio expected return: ', (-0.5 * risk_free_rate + 1.5 * max_return) * 10000/100.00, "%"
print ('\tPortfolio expected return: {:.3f}%').format((-0.5 * risk_free_rate + 1.5 * max_return) * 100.00)
#print '\tPortfolio standard deviation: ', (1.5 * np.sqrt(max_risk))* 10000/100.00, "%"
print ('\tPortfolio standard deviation: {:.3f}%').format((1.5 * np.sqrt(max_risk)) * 100.00)
