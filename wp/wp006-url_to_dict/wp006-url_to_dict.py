# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 09:01:42 2019

@author: anewbegin
"""
"""
Step 1: Import modules and get CWD & predecesors
"""
import os
import pandas as pd
import requests
import io

cwd = os.getcwd()
fileDir = os.path.dirname(os.path.abspath(cwd))
parentDir = os.path.dirname(fileDir)
#gparentDir = os.path.dirname(parentDir)

print(cwd)
print(fileDir)
print(parentDir)
#print(gparentDir)

#%% Step 2: Read in ticker config file - list of tickers
filepath = r'data\001-vanguard_etf_list\cln\etf_list.csv'
filename = os.path.join(parentDir, filepath)

colnames = ['ticker', 'name', 'asset_class', 'subclass']
data = pd.read_csv(filename, names=colnames, encoding = 'ISO-8859-1')

tickers = data.ticker.tolist()
del tickers[0]

print(tickers[1:10])
#print(filename)
#print(data)
#print(tickers)

#%% Step 3: Build master Adj. Close DataFrame
dt1 = "20110131"
dt2 = "20190531"

colnames = ['Date'] + tickers
masterAdjClose = pd.DataFrame([], columns=colnames)

masterAdjClose['Date'] = pd.date_range(start=dt1, end=dt2, freq='M')
masterAdjClose = masterAdjClose.sort_values(by='Date', ascending=False)

#print(masterAdjClose.head())

# %%
my_dict = {"A": masterAdjClose.loc[0:10,:], "B": masterAdjClose.loc[11:20,:]}

print(my_dict)

# %% Download data
my_empty_dict = {}
for ticker in tickers:
    url = 'https://stooq.com/q/d/l/?s=%s.us&d1=%s&d2=%s&i=m&o=1100000' % (ticker, dt1, dt2)
    urlReq = requests.get(url).content
    urlData = pd.read_csv(io.StringIO(urlReq.decode('utf-8')))
    urlData = urlData.sort_values(by='Date', ascending=False)
    
    filename = create_filename()
    data.to_csv(filename)
    my_empty_dict[ticker] = data
    
    
# %% Clean / process data
for data in my_empty_dict:
    clean_the_data()

# %% Combine
master_data = combine_individual_data()    
#%%
df = pd.DataFrame({'order_id': ['A', 'B'],
                   'items': [[{'item': 1, 'color': 'blue' },
                              {'item': 2, 'color': 'red'  }],
                             [{'item': 3, 'color': 'green'},
                              {'item': 2, 'color': 'pink' }]]},
                    columns= ['order_id', 'items'])
print(df)