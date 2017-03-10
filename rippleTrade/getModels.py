# -*- coding: utf-8 -*-
"""
Created on Fri Dec 16 12:21:14 2016

@author: AustinPeel
"""

import pandas as pd
#import stockLib
from rippleTrade import predictionLibrary , folderLocation , rippleLib
from sklearn.cross_validation import train_test_split


#import data from API
df = rippleLib.getData()

# save to CSV for R process
df.to_csv(folderLocation + "data/rip.csv")


#get the stock indicators
import subprocess
Rscript = "C:/Program Files/R/R-3.2.2/bin/Rscript"
subprocess.call([Rscript, folderLocation +'rippleR.R'] ,shell=True)

'''

df= df.join(stockLib.getTalibData(df).getSMA())
df= df.join(stockLib.getTalibData(df).getHT_Trend())
df= df.join(stockLib.getTalibData(df).getDX())
df= df.join(stockLib.getTalibData(df).getAD())
df= df.join(stockLib.getTalibData(df).getHT_DC())
df= df.join(stockLib.getTalibData(df).getATR())
df= df.join(stockLib.getTalibData(df).getBETA())
df= df.join(stockLib.getTalibData(df).getOBV())
df= df.join(stockLib.getTalibData(df).getNATR())
df= df.join(stockLib.getTalibData(df).getADX())
df= df.join(stockLib.getTalibData(df).getBOP())
df= df.join(stockLib.getTalibData(df).getAroonOsc())
df= df.join(stockLib.getTalibData(df).getCSL2())

'''

#bring data back in and save the last two dates to append to test data 
df = predictionLibrary.getdata()
df = df[df['newDate'].dt.year > 2013]
df= df.sort('newDate')
df2 = df.tail(2)
df3 = df.head(len(df.index)-2)


for p in ["buy","sell"]:
        
    
    # Keep same test and train data for all models so we can be consistent
    trainO, testO = train_test_split(df3, test_size = 0.3)
    testO = testO.append(df2)
    trainO = pd.DataFrame(trainO['newDate'])
    testO = pd.DataFrame(testO['newDate'])
    
    
    #make predicition and append to data frame. Get models, this appends to the Orignal Date.
    four, model4 =  predictionLibrary.makePredicitions(4,pred=p).getDDFPredicitions(df,trainO,testO)
    #fourS, model4S =  predictionLibrary.makePredicitions(4,pred="sell").getDDFPredicitions(df,trainO,testO)
    eight, model8 =  predictionLibrary.makePredicitions(8,pred=p).getDDFPredicitions(df,trainO,testO)
    twelve, model12 =  predictionLibrary.makePredicitions(12,pred=p).getDDFPredicitions(df,trainO,testO)
    sixteen, model16 = predictionLibrary.makePredicitions(16,pred=p).getDDFPredicitions(df,trainO,testO)
    
    m = pd.merge(four,four,on=['newDate'],how='inner')
    #get a df with all predicitions in one df
    total = pd.merge(four,eight, on=['newDate'],how='inner')
    total = pd.merge(total,twelve ,on=['newDate'],how='inner')
    total = pd.merge(total,sixteen ,on=['newDate'],how='inner')
    
    #make a final predicition
    rec2 = predictionLibrary.testFinalPrediction(total,df,p)    
    rec , model_all  = predictionLibrary.getFinalPrediction(total,df,p)
    
    
    #save models
    from sklearn.externals import joblib
    
    joblib.dump(model4.clf,folderLocation +"models/" + p + "/" + p + "model4clf.pk1") 
    joblib.dump(model4.clf,folderLocation +"models/" + p + "/" + p + "model8clf.pk1") 
    joblib.dump(model4.clf,folderLocation +"models/" + p + "/" + p + "model12clf.pk1") 
    joblib.dump(model4.clf,folderLocation +"models/" + p + "/" + p + "model16clf.pk1") 
    joblib.dump(model4.forest,folderLocation +"models/" + p + "/" + p + "model4rf.pk1") 
    joblib.dump(model4.forest,folderLocation +"models/" + p + "/" + p + "model8rf.pk1") 
    joblib.dump(model4.forest,folderLocation +"models/" + p + "/" + p + "model12rf.pk1")
    joblib.dump(model4.forest,folderLocation +"models/" + p + "/" + p + "model16rf.pk1") 
    joblib.dump(model_all.forest,folderLocation +"models/" + p + "/" + p + "modelallrf.pk1") 
    
