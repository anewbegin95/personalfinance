# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 12:04:13 2019

@author: anewbegin
"""
import pandas as pd
import requests
import io

tickers = ['EDV', 'BIV', 'VGIT', 'BLV', 'VGLT', 'VMBS', 'BSV', 'VTIP', 'VGSH', 'BND', 'VCIT', 'VCLT', 'VCSH', 'VTC', 'VTEB', 'VIG', 'ESGV', 'VUG', 'VYM', 'VV', 'MGC', 'MGK', 'MGV', 'VOO', 'VTI', 'VTV', 'VXF', 'VOO', 'VOT', 'VOE', 'VB', 'VBK', 'VBR', 'BNDW', 'BNDX', 'VWOB', 'VT', 'VSGX', 'VEU', 'VSS', 'VEA', 'VGK', 'VPL', 'VNQI', 'VIGI', 'VYMI', 'VXUS', 'VWOB', 'VOX', 'VCR', 'VDC', 'VDE', 'VFH', 'VHT', 'VIS', 'VGT', 'VAW', 'VNQ', 'VPU']
colnames = ['Date'] + tickers
#print(colnames)


dt1 = "20110131"
dt2 = "20190331"
url = 'https://stooq.com/q/d/l/?s=%s.us&d1=%s&d2=%s&i=m&o=1100000' % ('BLV', dt1, dt2)

urlData = requests.get(url).content
rawData = pd.read_csv(io.StringIO(urlData.decode('utf-8')))

#print(rawData.head())

df = pd.DataFrame([], columns=colnames)

df['BLV'] = rawData['Close']
df.BLV = df.BLV.astype(float)

df['Date'] = pd.date_range(start='1/31/2011', end='3/31/2019', freq='M')
df = df.sort_values(by='Date', ascending=False)

print(df.head())