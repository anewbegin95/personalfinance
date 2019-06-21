# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.

Notes:
There is no easy way to do RelPath in Python!
I wonder if there's a way to automate this to have it look at the # o/ hops
btwn the target and source paths and have 
"""
#import certifi
#import urllib3
#import sys
import os
import pandas as pd

"""
Step 1: Delete old single stock files
"""
fileDir = os.path.dirname(os.path.abspath(__file__))
parentDir = os.path.dirname(fileDir)
gparentDir = os.path.dirname(parentDir)

#print(__file__)
#print(fileDir)
#print(parentDir)
#print(gparentDir)

filepath = r'data\002-etf_hist_data\cln'
filename = os.path.join(gparentDir, filepath)
for the_file in os.listdir(filename):
    file_path = os.path.join(filename, the_file)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
        #elif os.path.isdir(file_path): shutil.rmtree(file_path)
    except Exception as e:
        print(e)

"""
Step 2: Read in ticker config file - list of tickers
"""
filepath = r'data\001-vanguard_etf_list\cln\etf_list.csv'
filename = os.path.join(gparentDir, filepath)

colnames = ['ticker', 'name', 'asset_class', 'subclass']
data = pd.read_csv(filename, names=colnames, encoding = 'ISO-8859-1')

tickers = data.ticker.tolist()
del tickers[0]

#print(filename)
#print(data)
#print(tickers)