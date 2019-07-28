# -*- coding: utf-8 -*-
# Created on Wed Apr  3 09:01:42 2019
# @author: anewbegin
# Step 1: Import modules and get CWD & predecesors

import os
import sys
from datetime import datetime
import pandas as pd
import requests
import io
from pandas_datareader import data
from bs4 import BeautifulSoup
import re
from time import mktime

fileDir = os.path.abspath(os.path.dirname(sys.argv[0]))
parentDir = os.path.dirname(fileDir)
gparentDir = os.path.dirname(parentDir)

#print(fileDir)
#print(parentDir)
#print(gparentDir)

# %% Step #: Read in ticker config file - list of tickers
filepath = r'data/001-vanguard_etf_list/cln/etf_list.csv'
filename = os.path.join(fileDir, filepath)

colnames = ['ticker', 'name', 'asset_class', 'subclass']
data = pd.read_csv(filename, names=colnames, encoding='ISO-8859-1')

tickers = data.ticker.tolist()
del tickers[0]

#print(tickers[1:10])
#print(filename)
#print(data)
print(tickers)

# %% Step #: Build ticker dictionary
day_begin='01-01-2011'
day_end='01-07-2019'
ticker_dict = {"Date": pd.date_range(start=day_begin,
                                     end=day_end,
                                     freq='M'
                                     )[::-1],
               "A": tickers
               }
adjCloseDict = dict.fromkeys(tickers)
# print(ticker_dict)
print(adjCloseDict)
# %% Step #: get crumb and cookies for historical data csv download from yahoo
"""
parameters: stock - short-handle identifier of the company
returns: a tuple of header, crumb and cookie
"""


def _get_crumbs_and_cookies(stock):
    url = 'https://finance.yahoo.com/quote/{}/history?frequency=1mo'\
          .format(stock)
    with requests.session():
        header = {'Connection': 'keep-alive',
                  'Expires': '-1',
                  'Upgrade-Insecure-Requests': '1',
                  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) \
                   AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/54.0.2840.99 Safari/537.36'
                  }
        website = requests.get(url, headers=header)
        soup = BeautifulSoup(website.text, 'lxml')
        crumb = re.findall('"CrumbStore":{"crumb":"(.+?)"}', str(soup))

        return (header, crumb[0], website.cookies)

# %% Step #: converts date to unix timestamp
#            parameters: date - in format (dd-mm-yyyy)
#            returns integer unix timestamp


def convert_to_unix(date):

    datum = datetime.strptime(date, '%d-%m-%Y')

    return int(mktime(datum.timetuple()))
# %% Step #:  queries yahoo finance api to receive historical data in csv frmt
"""
parameters:
    stock - short-handle identifier of the company
    interval - 1d, 1wk, 1mo - daily, weekly monthly data
    day_begin - starting date for the historical data (format: dd-mm-yyyy)
    day_end - final date of the data (format: dd-mm-yyyy)
returns: a list of comma seperated value lines
"""


def load_csv_data(stock,
                  interval='1mo',
                  day_begin='01-01-2011',
                  day_end='01-07-2019'
                  ):

    day_begin_unix = convert_to_unix(day_begin)
    day_end_unix = convert_to_unix(day_end)

    header, crumb, cookies = _get_crumbs_and_cookies(ticker)

    with requests.session():
        url = 'https://query1.finance.yahoo.com/v7/finance/download/' \
              '{stock}?'\
              'period1={day_begin}&period2={day_end}&'\
              'interval={interval}'\
              '&events=history&crumb={crumb}' \
              .format(stock=stock,
                      day_begin=day_begin_unix,
                      day_end=day_end_unix,
                      interval=interval,
                      crumb=crumb
                      )

        website = requests.get(url, headers=header, cookies=cookies)

        return website.text.split('\n')[:-1]
# %% Step 5: Download data and zip to dictionary
for ticker in tickers:
    adjCloseDict[ticker] = load_csv_data(ticker)['Adj Close']
# %%
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
