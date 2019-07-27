import pandas as pd
import pandas_datareader as pdr
import datetime

# Set dates
start = datetime.datetime(2018, 6, 1)
end = datetime.datetime(2019, 6, 1)

current_data = pd.read_excel('stock-names.xlsx', sheet_name='Sheet1')
# Initialize an empty dataframe for storing valid data
valid_data = []

counter = 1

for stock in current_data['Ticker']:
    stock = stock.encode('ascii','ignore')
    try:
        pdr.get_data_yahoo(stock, start=start, end=end, interval='m')
    except (KeyError, pdr._utils.RemoteDataError) as e:
        # If invalid, try next one
        print ('failed')
        continue

    valid_data.append(stock)
    counter = counter + 1
    if counter >= 5:
        break

# Store data into an excel under one column
pd.DataFrame({'StockNames': valid_data}).to_excel('valid-stock-names.xlsx')
