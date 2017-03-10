# -*- coding: utf-8 -*-
"""
Created on Tue Dec 20 13:17:50 2016

@author: AustinPeel
"""
from sklearn.metrics import roc_auc_score as AUC
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
import pandas as pd
import numpy as np 
from sklearn.cross_validation import train_test_split

def getdata(change=.01):
    df2 = pd.read_csv('rip.csv')
    df2['gain'] = (df2['open']-df2['close'])/df2['open']
    df2['buy'] = np.where(df2['gain']>=change, 1, 0)
    df2['sell'] = np.where(df2['gain']<=(-1*change), 1, 0)
    df2['newDate'] = pd.to_datetime(df2['start'], format ="%Y-%m-%dT%H:%M:%S%fZ",errors="ignore")
    return df2
    
def getFinalPrediction(df, dfOrig, pred):
    cols=['newDate',pred]
    buy = dfOrig[cols]
    buy['newDate'] = buy['newDate'] -  pd.to_timedelta(4, unit='h')
    total =pd.merge(df,buy ,on=['newDate'],how='left')
    total= total.sort('newDate')
    test = total.tail(1)
    train = total.dropna()   
    feature_cols = [col for col in train.columns if col not in ['newDate',pred]]
    model_all =models(feature_cols=feature_cols,test=test,train=train,predictor=pred)
    model_all.getRF()
    X_test = test[feature_cols]
    recommendation = model_all.forest.predict(X_test) 
    print test['newDate']
    return recommendation , model_all

def testFinalPrediction(df, dfOrig, pred):
    cols=['newDate',pred]
    buy = dfOrig[cols]
    buy['newDate'] = buy['newDate'] -  pd.to_timedelta(4, unit='h')
    total =pd.merge(df,buy ,on=['newDate'],how='left')  
    train, test = train_test_split(total, test_size = 0.3)
    feature_cols = [col for col in train.columns if col not in ['newDate',pred]]
    model_all =models(feature_cols=feature_cols,test=test,train=train,predictor=pred)
    model_all.getRF()
    X_test = test[feature_cols]
    recommendation = model_all.forest.predict_proba(X_test)
    aucRF = AUC(model_all.y_test.values,model_all.rf_p[:,1] )
    print aucRF     
    return recommendation
    
class makePredicitions:
    
    def __init__(self,hours,pred):
        self.hours = hours
        self.pred = pred
    
    def getDDFPredicitions(self,df,trainO,testO):
        df2 =self.setDataBack(df)
        trainO['newDate'] = trainO['newDate']  -  pd.to_timedelta(4, unit='h')
        testO['newDate'] = testO['newDate']  -  pd.to_timedelta(4, unit='h')
        train = pd.merge(trainO,df2, on="newDate",how="left")
        train = train.dropna()
        test = pd.merge(testO,df2, on="newDate",how="left")
        test = test.dropna()    
        feature_cols = [col for col in train.columns if col not in ['newDate','buy','sell']]
        model_4 =models(feature_cols=feature_cols,test=test,train=train,predictor=self.pred)
        model_4.testRF()
        model_4.testNB()
        four = self.getMergedData(model_4,test)
        #del four[self.pred]
        four['newDate'] = four['newDate'] +  pd.to_timedelta(self.hours, unit='h')
        return four, model_4
      
    def getMergedData(self,model,test):
        four = model.mergeRFToTest(test,self.hours)
        cols = ["RFprediction"+str(self.hours),self.pred,"newDate"]
        four = four[cols]
        temp = model.mergeNBToTest(test,self.hours)
        cols = ["NBprediction" +str(self.hours),self.pred,"newDate"]
        temp = temp[cols]
        four = pd.merge(four, temp, on=["newDate",self.pred],how="left")
        four = four.dropna()
        return four
    
    def setDataBack(self,df2):   
        predictors = ['buy','sell','newDate']
        pred = df2[predictors]
        #cols = ['newDate','SMA','DX','AD','HT_D','ATR','BETA','OBV','NATR','ADX','BOP','Aroon','gain']
        cols = ['newDate','rsi',	'aroonUp',	'oscillator'	,'macd',	'signal',	'obv',	'fastK','stochWPR'	,'ad'	,'cmf',	'tr',	'atr',	'trueHigh',	'trueLow',	'dn',	'mavg','pctB',	'cci',	'DIp',	'DIn',	'DX','ADX','roc']
        new = df2[cols]
        pred['newDate'] = pred['newDate'] -  pd.to_timedelta(self.hours, unit='h')
        a = new.merge(pred, how='left', on='newDate')
        b = a.dropna()
        return b
    
    def getLast(self,df):
        #cols = cols = ['SMA','DX','AD','HT_D','ATR','BETA','OBV','NATR','ADX','BOP','Aroon','gain'] 
        cols = ['rsi',	'aroonUp',	'oscillator'	,'macd',	'signal',	'obv',	'fastK','stochWPR'	,'ad'	,'cmf',	'tr',	'atr',	'trueHigh',	'trueLow',	'dn',	'mavg','pctB',	'cci',	'DIp',	'DIn',	'DX','ADX','roc']
        last = df.tail(1)
        last = last[cols]
        return last

class models():
    
    def __init__(self,feature_cols,test,train,predictor):
        self.X_train = train[feature_cols]
        self.X_test = test[feature_cols]
        self.y = train[predictor]
        self.y_test = test[predictor]    
    
    def getRF(self):
        forest = RandomForestClassifier( n_estimators = 1000, n_jobs = -1, verbose = 1 )
        self.forest = forest.fit( self.X_train, self.y )
        self.rf_p = self.forest.predict_proba( self.X_test )
        #self.aucRF = AUC( self.y_test.values, self.rf_p[:,1] )
        #print self.aucRF 
        return  self.rf_p
        
    def getNB(self):
        self.clf = GaussianNB()
        self.clf.fit(self.X_train, self.y)
        self.NB_p = self.clf.predict_proba(self.X_test)
        #self.aucNB = AUC( self.y_test.values, self.NB_p[:,1] )
        #print self.aucNB
        return self.rf_p
    
    def mergeRFToTest(self,test,hour):
        d = pd.DataFrame(self.rf_p)
        d.rename(columns={1 : "RFprediction" + str(hour) }, inplace=True)
        test.reset_index(drop=True, inplace=True)    
        test = pd.concat( [test, d["RFprediction" + str(hour)]], axis=1) 
        return test
        
    def mergeNBToTest(self,test,hour):
        d = pd.DataFrame(self.NB_p)
        d.rename(columns={1 : "NBprediction"+ str(hour)}, inplace=True)
        test.reset_index(drop=True, inplace=True)    
        test = pd.concat( [test, d["NBprediction" + str(hour)]], axis=1) 
        return test

    def testRF(self):
        forest = RandomForestClassifier( n_estimators = 1000, n_jobs = -1, verbose = 1 )
        self.forest = forest.fit( self.X_train, self.y )
        self.rf_p = self.forest.predict_proba( self.X_test )
        self.aucRF = AUC( self.y_test.values, self.rf_p[:,1] )
        print self.aucRF 
        return  self.rf_p
        
    def testNB(self):
        self.clf = GaussianNB()
        self.clf.fit(self.X_train, self.y)
        self.NB_p = self.clf.predict_proba(self.X_test)
        self.aucNB = AUC( self.y_test.values, self.NB_p[:,1] )
        print self.aucNB
        return self.rf_p