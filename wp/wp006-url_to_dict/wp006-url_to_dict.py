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

    for key in adjCloseDict.keys():
        if ticker != key:
            next
        else:
            adjCloseDict[ticker] = urlCloseList
# print(adjCloseDict)
# %% Clean / process data
for data in my_empty_dict:
    clean_the_data()

# %% Combine
master_data = combine_individual_data()
#%% Test to see how dictionaries work
df = pd.DataFrame({'order_id': ['A', 'B'],
                   'items': [[{'item': 1, 'color': 'blue'},
                              {'item': 2, 'color': 'red'}],
                             [{'item': 3, 'color': 'green'},
                              {'item': 2, 'color': 'pink'}]]},
    columns= ['order_id','items'])
print(df)
