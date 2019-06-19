# -*- coding: utf-8 -*-
"""
Created on Monday Jan 21 16:14:04 2019

@author: anewbegin


Notes:
There is no easy way to do RelPath in Python!
I wonder if there's a way to automate this to have it look at the # o/ hops
btwn the target and source paths and have 
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
gparentDir = os.path.dirname(parentDir)

#print(cwd)
#print(fileDir)
#print(parentDir)
#print(gparentDir)

#%% Step 2: Read in ticker config file - list of tickers
filepath = r'data\001-vanguard_etf_list\cln\etf_list.csv'
filename = os.path.join(gparentDir, filepath)

colnames = ['ticker', 'name', 'asset_class', 'subclass']
data = pd.read_csv(filename, names=colnames, encoding = 'ISO-8859-1')

tickers = data.ticker.tolist()
del tickers[0]

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


#%% Step 4: Read Adj. Close data into DataFrame from STOOQ.com url
for ticker in tickers[0:10]:
    url = 'https://stooq.com/q/d/l/?s=%s.us&d1=%s&d2=%s&i=m&o=1100000' % (ticker, dt1, dt2)
#    filename = r'C:\Users\anewbegin\Documents\Personal\personalfinance\data\002-etf_hist_data\cln\%s.csv' % ticker.lower()
    
    urlReq = requests.get(url).content
    urlData = pd.read_csv(io.StringIO(urlReq.decode('utf-8')))
#    print(urlData.head())
    urlData = urlData.sort_values(by='Date', ascending=False)

    for name in colnames:
        if name == ticker:
            masterAdjClose[name] = urlData['Close']
#            masterAdjClose.name = masterAdjClose.name.astype(float)
print(masterAdjClose.head())

#%% Step 5: Print master Adj. Close DataFrame into .csv
filepath = r'data\002-etf_hist_data\cln\masterAdjClose.csv'
filename = os.path.join(gparentDir, filepath)
masterAdjClose.to_csv(filename,index=False)

#%%
#filepath = r'data\002-etf_hist_data\cln'
#filename = os.path.join(gparentDir, filepath)
#for the_file in os.listdir(filename):
#    file_path = os.path.join(filename, the_file)
#    try:
#        if os.path.isfile(file_path):
#            os.unlink(file_path)
#        #elif os.path.isdir(file_path): shutil.rmtree(file_path)
#    except Exception as e:
#        print(e)

