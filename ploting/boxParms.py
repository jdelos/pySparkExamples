# -*- coding: utf-8 -*-
"""
Created on Wed Nov 02 11:12:52 2016

Spark module that computes the parameters to generate a box plot.
The box plot paramters are computed by grouping the values of the input
spark dataframe by key.

The operation is rather slow since it needs to collect the values in memory to use the numpy percentile
functions.


@author: julia.delos
"""
import numpy as np

#Compute box parameters using numpy
def boxParams(v):
    """
        Compute the parameters of a box plot using numpy from
        the data set in the list v.

        Returns a list with the following values
        [
         Q1 --> First percentile 25%
         Q2 --> Second percentile or median
         Q3 --> Third percentile, 75%
         IQR --> Interpercneitle range 50% of the data relines inside this range.
         Qmin --> Minimum value of the dataset without the outliners
         Qmax --> Maximum value of the dataset without the outliners
         OL   --> List the list of otuliners (if there are any).

    """
    v = np.array(v)
    Q1 = float(np.percentile(v,25))
    Q3 = float(np.percentile(v,75))
    Q2 = float(np.median(v))
    IQR = Q3 - Q1
    vCl =  v[(v>Q1-1.5*IQR) & (v<Q3+1.5*IQR)]
    OL = v[(v<Q1-1.5*IQR) | (v>Q3+1.5*IQR)]
    Qmax = float(np.max(vCl))
    Qmin = float(np.min(vCl))
    return [Q1,Q2,Q3,IQR,Qmax,Qmin,OL.tolist()]

def boxPerKey(df,keyCol,valCol):
    """
    This function computes the box plot paramters from the data frame df,
     given that
        keyCol is the column index for the keys and
        valCol is the column index for the values.

    The function retursn a spark dataframe with the following schema:
        DataFrame[key: [type inherited from the key],
                   Q1: double,
                   Q2: double,
                   Q3: double,
                   IQR: double,
                   Qmax: double,
                   Qmin: double,
                   OL: array<double>]

    For example considering that we have the memory data frame queried as:
        df = sqlContext.sql("SELECT app_str, pm FROM postnl_struct.srvchecks_mem")
        boxPrms =  boxPerKey(df,0,1)
    in this case
        app_str is the key, hence column index 0
        pm is the value, hence column index 1
    """

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
                      

# Test module only runs if this scritp is runed as main program
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
  
  
 
