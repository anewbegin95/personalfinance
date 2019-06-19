# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 16:14:04 2019

@author: anewbegin
"""

import pandas as pd

path = r"C:\Users\anewbegin\Documents\Personal\personalfinance\data\003-fama_french_factors_data\cln\fama_french_factors.csv"

DF = pd.read_csv(path, error_bad_lines=False, encoding="ISO-8859-1")
print(DF.head())
