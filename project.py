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
        # Uncomment and change to 'W' you want weekly, 'M' for monthly or 'Y' for yearly returns
        df = pdr.get_data_yahoo(stock_code_1, start=start, end=end, interval='m')

        # df = pdr.DataReader(stock_code_1, 'yahoo', start, end)
        # df = df.groupby(pd.Grouper(freq='M')).mean()

        stock_1 = df['Adj Close']
    except (KeyError, pdr._utils.RemoteDataError) as e:

        # If invalid, as for a good stock code

        continue
    break

# Read data for stock 2
stock_code_2 = raw_input("Stock code name 2: ")
while True:
    try:
        df = pdr.get_data_yahoo(stock_code_2, start=start, end=end, interval='m')

        stock_2 = df['Adj Close']
    except (KeyError, pdr._utils.RemoteDataError) as e:
        stock_code_2 = raw_input("Enter a valid code for Stock 2: ")
        continue
    break

# Get risk-free rate from input
risk_free_string = raw_input("Risk Free Rate (Annual) (in percentage form ex. 5.25%): ")
while True:
    try:
        # Parse for percentage
        risk_free_rate = float(re.findall(r'(\d+(\.\d+)?%)', risk_free_string)[0][0].rstrip("%"))/100.0000
    except IndexError:
        # Ask again if not valid
        risk_free_string = raw_input("Please enter a percentage value of the form X.XX%: ")
        continue
    break

# Get monthly risk free rate
risk_free_rate_monthly = np.power([risk_free_rate+1], [1.0/12.0])[0] -1

# Calculate returns for both stocks
returns_monthly_1 = stock_1.pct_change()
returns_monthly_2 = stock_2.pct_change()

# Calculate statistics for returns
average_return_monthly_1 = returns_monthly_1.mean()
average_return_monthly_2 = returns_monthly_2.mean()

# Annual returns
average_return_annual_1 = (1 + average_return_monthly_1)**12 - 1
average_return_annual_2 = (1 + average_return_monthly_2)**12 - 1

variance_monthly_1 = returns_monthly_1.var()
variance_monthly_2 = returns_monthly_2.var()

stdev_monthly_1 = returns_monthly_1.std()
stdev_monthly_2 = returns_monthly_2.std()

# [1:] because the first row is NAN since we are calculating the change of rate
covariances_monthly = np.cov(returns_monthly_1.to_numpy()[1:], returns_monthly_2.to_numpy()[1:])
covariances_annual = covariances_monthly * 12

variance_annual_1 = covariances_annual[0][0]
variance_annual_2 = covariances_annual[1][1]

stdev_annual_1  = np.sqrt(variance_annual_1)
stdev_annual_2  = np.sqrt(variance_annual_2)

covariance_monthly = covariances_monthly[0][1]
covariance_annual = covariances_annual[0][1]

# Min Variance Portfolio

# Generate weights of 2.5% interval
# weights_1 = np.array(list(range(0, 41)))*0.025
# weights_2 = 1 - weights_1
# weights = np.array([weights_1, weights_2]).T

# # port_returns = [np.matmul(w,returns.T) for w in weights]
# port_returns = [w[0] * average_return_annual_1 + w[1] * average_return_annual_2 for w in weights]
# # port_vars    = [np.matmul(np.matmul(w,covar),w.T) for w in weights]
# port_vars    = [w[0]**2*covariances_annual[0,0] + w[1]**2*covariances_annual[1,1] + 2*w[0]*w[1]*covariances_annual[0,1] for w in weights]
# port_sds     = [np.sqrt(v) for v in port_vars]

proportion_1 = (variance_monthly_2 - covariance_monthly)/(variance_monthly_1 + variance_monthly_2 - 2*covariance_monthly)
if(proportion_1 > 1):
    proportion_1 = 1;
if(proportion_1 < 0):
    proportion_1 = 0;
proportion_2 = (1 - proportion_1)

mvp_return = proportion_1 * average_return_monthly_1 + proportion_2 * average_return_monthly_2
mvp_risk = np.sqrt(proportion_1**2 * variance_monthly_1 + proportion_2**2 * variance_monthly_2 + 2 * proportion_1 * proportion_2 * covariance_monthly)

# Annual minimum variance portfolio
proportion_annual_1 = (variance_annual_2 - covariance_annual)/(variance_annual_1 + variance_annual_2 - 2*covariance_annual)
if(proportion_annual_1 > 1):
    proportion_annual_1 = 1;
if(proportion_annual_1 < 0):
    proportion_annual_1 = 0;
proportion_annual_2 = (1 - proportion_annual_1)

mvp_return_annual = proportion_annual_1 * average_return_annual_1 + proportion_annual_2 * average_return_annual_2
mvp_risk_annual = np.sqrt(proportion_annual_1**2 * variance_annual_1 + proportion_annual_2**2 * variance_annual_2 + 2 * proportion_annual_1 * proportion_annual_2 * covariance_annual)

# Display minimum variance portfolio

print('')
print('Minimum Variance Portfolio: ')
print('\tMVP monthly proportion {}: {:.3f}%').format(stock_code_1, proportion_1 * 100.00)
print('\tMVP monthly proportion {}: {:.3f}%').format(stock_code_2, proportion_2 * 100.00)
print('\tMVP monthly standard deviation: {:.3f}%').format(mvp_risk * 100.00)
print('\tMVP monthly standard portfolio return: {:.3f}%').format(mvp_return * 100.00)
print('\tMVP annual proportion {}: {:.3f}%').format(stock_code_1, proportion_annual_1 * 100.00)
print('\tMVP annual proportion {}: {:.3f}%').format(stock_code_2, proportion_annual_2 * 100.00)
print('\tMVP annual standard deviation: {:.3f}%').format(mvp_risk_annual * 100.00)
print('\tMVP annual standard portfolio return: {:.3f}%').format(mvp_return_annual * 100.00)


# Maximize Sharpe Ratio

w_1 = 0.0
w_2 = 1.0

max_r = (w_1 * average_return_monthly_1 + w_2 * average_return_monthly_2 - risk_free_rate_monthly) / np.sqrt(w_1**2 * variance_monthly_1 + w_2**2 * variance_monthly_2 + 2 * w_1 * w_2 * covariance_monthly)
max_w1 = 0.0
max_w2 = 1.0

for x in range(0, 10000):
    w_1 = w_1 + 0.0001
    w_2 = w_2 - 0.0001
    e_rp = w_1 * average_return_monthly_1 + w_2 * average_return_monthly_2
    excess_return = e_rp - risk_free_rate_monthly
    sharpe_ratio = excess_return / np.sqrt(w_1**2 * variance_monthly_1 + w_2**2 * variance_monthly_2 + 2 * w_1 * w_2 * covariance_monthly)

    if(sharpe_ratio > max_r):
        max_r = sharpe_ratio
        max_w1 = w_1
        max_w2 = w_2

max_return = (max_w1 * average_return_monthly_1 + max_w2 * average_return_monthly_2)
max_risk = np.sqrt(max_w1 ** 2 * variance_monthly_1 + max_w2 ** 2 * variance_monthly_2 + 2 * max_w1 * max_w2 * covariance_monthly)

# Annual Sharpe Ratio
w_annual_1 = 0.0
w_annual_2 = 1.0

max_annual_r = (w_annual_1 * average_return_annual_1 + w_annual_2 * average_return_annual_2 - risk_free_rate) / np.sqrt(w_annual_1**2 * variance_annual_1 + w_annual_2**2 * variance_annual_2 + 2 * w_annual_1 * w_annual_2 * covariance_annual)
max_annual_w1 = 0.0
max_annual_w2 = 1

for x in range(0, 10000):
    w_annual_1 = w_annual_1 + 0.0001
    w_annual_2 = w_annual_2 - 0.0001
    e_rp = w_annual_1 * average_return_annual_1 + w_annual_2 * average_return_annual_2
    excess_return = e_rp - risk_free_rate
    sharpe_ratio = excess_return / np.sqrt(w_annual_1**2 * variance_annual_1 + w_annual_2**2 * variance_annual_2 + 2 * w_annual_1 * w_annual_2 * covariance_annual)

    if(sharpe_ratio > max_annual_r):
        max_annual_r = sharpe_ratio
        max_annual_w1 = w_annual_1
        max_annual_w2 = w_annual_2

max_return_annual = (max_annual_w1 * average_return_annual_1 + max_annual_w2 * average_return_annual_2)
max_risk_annual = np.sqrt(max_annual_w1 ** 2 * variance_annual_1 + max_annual_w2 ** 2 * variance_annual_2 + 2 * max_annual_w1 * max_annual_w2 * covariance_annual)

# Print out cases

print ('')
print ('Case 1: ')
print ('\tGiven-Proportion invested in risk-free asset: 0%')
print ('\tGiven-Proportion invested in market portfolio: 100%')
print ('')
print ('\tMaximum Sharpe ratio: {:.3f}').format(max_r)
print ('\tMarket portfolio proportion {}: {:.3f}%').format(stock_code_1, max_w1 * 100.00)
print ('\tMarket portfolio proportion {}: {:.3f}%').format(stock_code_2, max_w2 * 100.00)
print ('\tMarket monthly portfolio expected return: {:.3f}%').format(max_return * 100.00)
print ('\tMarket monthly portfolio standard deviation: {:.3f}%').format(max_risk * 100.00)
print ('\tMarket annual portfolio expected return: {:.3f}%').format(max_return_annual * 100.00)
print ('\tMarket annual portfolio standard deviation: {:.3f}%').format(max_risk_annual * 100.00)

print ('')
print ('Case 2: ')
print ('\tGiven-Proportion invested in risk-free asset: 50%')
print ('\tGiven-Proportion invested in market portfolio: 50%')
print ('')
print ('\tPortfolio monthly expected return: {:.3f}%').format((0.5 * max_return + 0.5 * risk_free_rate_monthly) * 100.00)
print ('\tPortfolio monthly standard deviation: {:.3f}%').format((0.5 * max_risk) * 100.00)
print ('\tPortfolio annual expected return: {:.3f}%').format((0.5 * max_return_annual + 0.5 * risk_free_rate) * 100.00)
print ('\tPortfolio annual standard deviation: {:.3f}%').format((0.5 * max_risk_annual) * 100.00)

print ('')
print ('Case 3: ')
print ('\tGiven-Proportion invested in risk-free asset: -50%')
print ('\tGiven-Proportion invested in market portfolio: 150%')
print ('')
print ('\tPortfolio monthly expected return: {:.3f}%').format((-0.5 * risk_free_rate_monthly + 1.5 * max_return) * 100.00)
print ('\tPortfolio monthly standard deviation: {:.3f}%').format((1.5 * max_risk) * 100.00)
print ('\tPortfolio annual expected return: {:.3f}%').format((-0.5 * risk_free_rate + 1.5 * max_return_annual) * 100.00)
print ('\tPortfolio annual standard deviation: {:.3f}%').format((1.5 * max_risk_annual) * 100.00)
