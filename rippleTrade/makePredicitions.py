# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 09:35:53 2017

@author: AustinPeel
"""

from rippleTrade import rippleLib 
from rippleTrade.predictionLibrary import getdata
from sklearn.externals import joblib

#get latest data
df = rippleLib.getData()

# save to CSV for R process
df.to_csv("rip.csv")


#get the stock indicators
import subprocess
Rscript = "C:/Program Files/R/R-3.2.2/bin/Rscript"
subprocess.call([Rscript, 'rippleR.R'] ,shell=True)

#bring data back in and save the last two dates to append to test data 
df = getdata()

records= []
for n in [1,2,3,4]:
    a = rippleLib.getDFforPrediciting(df,n)
    records.append(a)

c = joblib.load('models/model4rf.pk1') 
rf4 = c.predict_proba(records[0])
c = joblib.load('models/model4clf.pk1') 
clf4 = c.predict_proba(records[0])
c = joblib.load('models/model8rf.pk1') 
rf8 = c.forest.predict_proba(records[1])
c = joblib.load('models/model8clf.pk1') 
clf8 = c.clf.predict_proba(records[1])
c = joblib.load('models/model12rf.pk1') 
rf12 =c.forest.predict_proba(records[2])
c = joblib.load('models/model12clf.pk1') 
clf12 = c.clf.predict_proba(records[2])
c = joblib.load('models/model16rf.pk1') 
rf16 = c.forest.predict_proba(records[3])
c = joblib.load('models/model16clf.pk1') 
clf16 = c.clf.predict_proba(records[3])
c = joblib.load('models/model4clf.pk1') 
c.predict_proba(records[0])