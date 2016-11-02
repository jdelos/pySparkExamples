# -*- coding: utf-8 -*-
"""
Created on Wed Nov 02 11:12:52 2016

@author: julia.delos
"""
import numpy as np

#Compute box parameters using numpy
def boxParams(v):
    Q1 = np.percentile(v,25)
    Q3 = np.percentile(v,75)
    Q2 = np.median(v)
    IQR = Q3 - Q1
    vCl = v[(v>Q1-1.5*IQR) & (v<Q3+1.5*IQR)]
    vOut = v[(v<Q1-1.5*IQR) | (v>Q3+1.5*IQR)]
    Qmax = np.max(vCl)
    Qmin = np.min(vCl)
    return [Q1,Q2,Q3,IQR,Qmax,Qmin,vOut]



def boxPerKey(df,keyCol,valCol):
     
    
    #I converter the data frame to an rdd
    rdd = df.rdd
    # The datafram is maped to a list of tupples as
    # (key,val)
    rddKeyValue = rdd.map(lambda x: (x[keyCol],x[valCol]))
    # Collect the list of unique keys
    keys = rdd.map(lambda x: x[keyCol]).distinct().collect()
    # Iterate throught all keys    
    boxParams =dict()#Create a dictonary sotring all values
    for key in Keys:
        #Collect the values to a vector         
        valVect = rddKeyValue.filter(lambda pair: pair[0]==key)
                             .map(lambda pair: pair[1])
                             .collect()
        #Compute the box parameters                      
        boxParms[key] = boxParams(valVect)
    return rdd.context.sc
                      .parallelize([[k] + v for k, v in boxParams.items()])
                      .toDF['key','Q1','Q2','Q3','IQR','OL']
                      
    
    
    