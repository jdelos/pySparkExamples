# -*- coding: utf-8 -*-


"""
Created on Wed Nov 02 11:12:52 2016

@author: julia.delos
"""
import numpy as np

#Compute box parameters using numpy
def boxParams(v):
    v = np.array(v)
    Q1 = float(np.percentile(v,25))
    Q3 = float(np.percentile(v,75))
    Q2 = float(np.median(v))
    IQR = Q3 - Q1
    vCl =  v[(v>Q1-1.5*IQR) & (v<Q3+1.5*IQR)]
    vOut = v[(v<Q1-1.5*IQR) | (v>Q3+1.5*IQR)]
    Qmax = float(np.max(vCl))
    Qmin = float(np.min(vCl))
    return [Q1,Q2,Q3,IQR,Qmax,Qmin,vOut.tolist()]



def boxPerKey(df,keyCol,valCol):
    #I converter the data frame to an rdd
    rdd = df.rdd
    # The datafram is maped to a list of tupples as
    # (key,val)
    rddKeyValue = rdd.map(lambda x: (x[keyCol],x[valCol]))
    rddKeyValue.cache()
    # Collect the list of unique keys
    keys = rdd.map(lambda x: x[keyCol]).distinct().collect()
    # Iterate throught all keys    
    params =dict()  #Create a dictonary sotring all values
    for key in keys:
        #Collect the values to a vector         
        valVect = rddKeyValue.filter(
                  lambda pair: pair[0]==key
                  ).map(
                  lambda pair: pair[1]
                  ).collect()
        #Compute the box parameters                      
        params[key] = boxParams(valVect)
    return rdd.context.parallelize(
            [[k] + v for k, v in params.items()]
            ).toDF(['key','Q1','Q2','Q3','IQR','Qmax','Qmin','OL'])
                      
    
if __name__ == "__main__":
    from pyspark import SparkContext, HiveContext
    print(">>>>> Loading SparkContext")
    sc = SparkContext("local",appName = "TestScript")
    print(">>>>> Loading HiveContext")
    sqlContext = HiveContext(sc)
    sc.setLogLevel('ERROR')  #Reduce logging level
    df = sqlContext.sql("SELECT app_str, pm FROM postnl_struct.srvchecks_mem")
    df_flt = df.filter(df.app_str == 'PAK')
    df_out = boxPerKey(df_flt,0,1)
    df_out.show()
  
  
 
