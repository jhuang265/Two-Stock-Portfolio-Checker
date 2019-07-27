import pandas as pd
import pandas_datareader as pdr
import datetime
import re
import numpy as np

# Set dates
start = datetime.datetime(2018, 6, 1)
end = datetime.datetime(2019, 6, 1)

all_returns_monthly = []

stock_code =  raw_input("Stock code name: ")

counter = 0

# Read data for stock
while True:
    try:
        # Uncomment and change to 'W' you want weekly, 'M' for monthly or 'Y' for yearly returns
        if(counter >= 10):
            break

        if(stock_code == 'done'):
            break;

        df = pdr.get_data_yahoo(stock_code, start=start, end=end, interval='m')

        # df = pdr.DataReader(stock_code_1, 'yahoo', start, end)
        # df = df.groupby(pd.Grouper(freq='M')).mean()

        all_returns_monthly.append(df['Adj Close'])
        counter = counter + 1
        stock_code = raw_input("Enter a code for the next stock: ")
        continue;
    except (KeyError, pdr._utils.RemoteDataError) as e:

        # If invalid, as for a good stock code
        stock_code = raw_input("Enter a valid code for the stock: ")
        continue
    break

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

# print all_returns_monthly

# Get monthly risk free rate
risk_free_rate_monthly = np.power([risk_free_rate+1], [1.0/12.0])[0] -1

returns_monthly = []
for stock in all_returns_monthly:
    returns_monthly.append(stock.pct_change()[1:])

average_returns_monthly = []
variance_monthly = []
std_monthly = []
returns_annual = []

for i in range(0, len(returns_monthly)):
    average_returns_monthly.append(returns_monthly[i].mean())
    variance_monthly.append(returns_monthly[i].var())
    std_monthly.append(returns_monthly[i].std())

for i in range(0, len(average_returns_monthly)):
    returns_annual.append((1+average_returns_monthly[i])**12 - 1)

covariances_monthly = []

for i in range(0, len(returns_monthly)):
    variances = []
    for j in range(0, len(returns_monthly)):
        variances.append(np.cov(returns_monthly[i].to_numpy(), returns_monthly[j].to_numpy())[0][1])
    covariances_monthly.append(variances)

covariances_annual = []
for i in covariances_monthly:
    variances= []
    for j in i:
        variances.append(j*12)
    covariances_annual.append(variances)

