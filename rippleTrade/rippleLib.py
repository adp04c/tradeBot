# -*- coding: utf-8 -*-
"""
Created on Mon Dec 19 08:44:53 2016

@author: AustinPeel
"""

from datetime import datetime, timedelta
import re
import pandas as pd

def addFourHours(date):
    a = str(datetime.strptime(date, "%Y-%m-%dT%H:%M:%S%fZ") + timedelta(hours=4))
    b = re.sub('\s',"T",a)
    b = b + "Z"
    return b

def getData():
    df = pd.read_csv("https://data.ripple.com/v2/exchanges/USD+rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B/XRP?interval=4hour&format=csv&limit=1000")
    maxDate = addFourHours(max(df['start']))
    string = "https://data.ripple.com/v2/exchanges/USD+rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B/XRP?interval=4hour&format=csv&limit=1000" + "&start=" + maxDate
    while True:
        df2 = pd.read_csv(string)
        df = pd.concat([df,df2])
        maxDate = addFourHours(max(df2['start']))
        a= datetime.strptime(maxDate, "%Y-%m-%dT%H:%M:%S%fZ")
        if datetime.today().date() == a.date():
            break
        string ="https://data.ripple.com/v2/exchanges/USD+rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B/XRP?interval=4hour&format=csv&limit=1000" + "&start=" + maxDate
    return df
    
def getDFforPrediciting(df,num): 
    cols = ['newDate','rsi',	'aroonUp',	'oscillator'	,'macd',	'signal',	'obv',	'fastK','stochWPR'	,'ad'	,'cmf',	'tr',	'atr',	'trueHigh',	'trueLow',	'dn',	'mavg','pctB',	'cci',	'DIp',	'DIn',	'DX','ADX','roc']
    new = df[cols]
    last =  new.tail(num)
    last = last.head(1)
    last1 = last.iloc[:,1:]
    return last1