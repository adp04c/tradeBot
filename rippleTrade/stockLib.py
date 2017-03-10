# -*- coding: utf-8 -*-
"""
Created on Mon Dec 19 11:21:30 2016

@author: austin
"""
import numpy
import pandas as pd
import talib

class getTalibData:
    
    def __init__(self,df):
        self.high = numpy.asarray(df['high'])
        self.low = numpy.asarray(df['low'])
        self.close = numpy.asarray(df['close'])
        self.open = numpy.asarray(df['open'])
        self.volume = numpy.asarray(df['base_volume'])
        #for i in dir(self):
        #   result = getattr(self, i)()
        #   print result
    #Momentum
    def getSMA(self):
        output = talib.SMA(self.close, 20)
        a=pd.DataFrame(output)
        a = a.rename(columns={0:"SMA"})
        return a
    
    def getADX(self):
        output = talib.ADX(self.high, self.low, self.close, timeperiod=14)
        a=pd.DataFrame(output)
        a = a.rename(columns={0:"ADX"})
        return a
    
    def getAroonOsc(self):
        output = talib.AROONOSC(self.high, self.low, timeperiod=14)
        a=pd.DataFrame(output)
        a = a.rename(columns={0:"Aroon"})
        return a
    
    def getBOP(self):
        output = talib.BOP(self.open, self.high, self.low, self.close)
        a=pd.DataFrame(output)
        a = a.rename(columns={0:"BOP"})
        return a
        
    def getDX(self):
        output = talib.DX(self.high, self.low, self.close, timeperiod=14)
        a=pd.DataFrame(output)
        a = a.rename(columns={0:"DX"})
        return a
    #Volumne
    def getAD(self):
        output = talib.AD(self.high, self.low, self.close, self.volume)
        a=pd.DataFrame(output)
        a = a.rename(columns={0:"AD"})
        return a
    
    def getOBV(self):
        output = talib.OBV(self.close, self.volume)
        a=pd.DataFrame(output)
        a = a.rename(columns={0:"OBV"})
        return a 
    #Volatility
    def getATR(self):
        output = talib.ATR(self.high, self.low, self.close, timeperiod=14)
        a=pd.DataFrame(output)
        a = a.rename(columns={0:"ATR"})
        return a
    
    def getNATR(self):
        output = talib.NATR(self.high, self.low, self.close, timeperiod=14)
        a=pd.DataFrame(output)
        a = a.rename(columns={0:"NATR"})
        return a
    #Cycles
    def getHT_DC(self):
        output = talib.HT_DCPERIOD(self.close)
        a=pd.DataFrame(output)
        a = a.rename(columns={0:"HT_D"})
        return a
    
    def getHT_Trend(self):
        output = talib.HT_TRENDMODE(self.close)
        a=pd.DataFrame(output)
        a = a.rename(columns={0:"HT_trend"})
        return a
    #Patterns
    def getCSL2(self):
        output = talib.CDL2CROWS(self.open, self.high, self.low, self.close)
        a=pd.DataFrame(output)
        a = a.rename(columns={0:"CSL2"})
        return a
    #Stats
    def getBETA(self):
        output = talib.BETA(self.high, self.low, timeperiod=5)
        a=pd.DataFrame(output)
        a = a.rename(columns={0:"BETA"})
        return a

    
    
    
    
        
    
    
    
    