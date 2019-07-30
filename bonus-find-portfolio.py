import pandas as pd
# import pandas_datareader as pdr
# import datetime
# import re
# import numpy as np

import evenPortfolioMod as epm

current_data = pd.read_excel('valid-stock-names.xlsx', sheet_name='Sheet1')

stockNames = current_data[['StockNames']].values.T[0].tolist()

# print("length: " + str(len(stockNames)))

portfolio = epm.genEvenPortfolio([stockNames[2], stockNames[3], stockNames[4], stockNames[5], stockNames[6]])
print ('ret: {} \trisk: {}'.format(portfolio['ret'], portfolio['risk']))

# for i in range(1, len(stockNames)):
#     for j in range(i, len(stockNames)):
#         for k in range(j, len(stockNames)):
#             for h in range(k, len(stockNames)):
#                 for l in range(h, len(stockNames)):
#                     portfolio = epm.genEvenPortfolio([stockNames[i], stockNames[j],
#                                    stockNames[k], stockNames[h], stockNames[l]])
#                     if portfolio['ret']
# epm.readStock()


