# -*- coding: utf-8 -*-
# Created on Wed Apr  3 09:01:42 2019
# @author: anewbegin
# Step 1: Import modules and get CWD & predecesors

import os
import sys
import pandas as pd
import requests
import io

fileDir = os.path.abspath(os.path.dirname(sys.argv[0]))
parentDir = os.path.dirname(fileDir)
gparentDir = os.path.dirname(parentDir)

print(fileDir)
print(parentDir)
print(gparentDir)

# %% Step 2: Read in ticker config file - list of tickers
filepath = r'data/001-vanguard_etf_list/cln/etf_list.csv'
filename = os.path.join(fileDir, filepath)

colnames = ['ticker', 'name', 'asset_class', 'subclass']
data = pd.read_csv(filename, names=colnames, encoding='ISO-8859-1')

tickers = data.ticker.tolist()
del tickers[0]

print(tickers[1:10])
print(filename)
print(data)
print(tickers)

# %% Step 3: Build ticker dictionary
dt1 = "20110131"
dt2 = "20190531"
ticker_dict = {"Date": pd.date_range(start=dt1, end=dt2, freq='M')[::-1],
               "A": tickers
               }
adjCloseDict = dict.fromkeys(tickers)
# print(ticker_dict)
print(adjCloseDict)

# %% Step 4: Download data and zip to dictionary

for ticker in tickers[0:10]:
    url = r'https://stooq.com/q/d/l/?s=%s.us&d1=%s&d2=%s&i=m&o=1100000' \
           % (ticker, dt1, dt2)

    urlReq = requests.get(url).content
    urlData = pd.read_csv(io.StringIO(urlReq.decode('utf-8')))

    urlCloseList = urlData['Close'].tolist()

#    print(urlCloseList[0:5])

#    for key in adjCloseDict.keys():
#        if ticker != key:
#            next
#        else:
    adjCloseDict[ticker] = urlCloseList
#%%
print(adjCloseDict)
# %% Next steps
# %%Convert data in adjusted close frame to % change from previous time period
    # Convert each list to a pandas data series
    # Iterate over each series using .pct_change() to get % difference
    # Reverse order of list (?)

# Bring Fama French Factor Data into a dataframe
# Cleanse FF5F data and convert to decimals
# Convert % change to % excess return using RF rate for period
# Append a single Int column with "1" val
# Run multivariable regression against each adj close colum w/ adj close as Y and FF5F as X
# Calculate Cost of Equity using avg of each coeff * each unique coeff + rfr (annualized)
# Create covariance table of each adj return column vs every other adj return column
# Optimize portfolio extected risk/return using COE and changes in # of share investments in securities
