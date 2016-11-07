"""
pySpark example how to use the boxParms spark module

In this case we generate the boxParmas for a sample data to make it run fast.

Run this example by executing this line:
    spark-commit pySpark_genBoxPrms.py

@author: julia.delos
"""


from pyspark import SparkContext, HiveContext

if __name__=="__main__":
    sc = SparkContext(master="yarn-client",appName="PythonStreamingWindowedWC_Cluster")
    sqlContex = HiveContext(sc)
    sc.setLogLevel('ERROR')

    #Add python module
    sc.addPyFile('boxParams.py')
    from boxParams import boxPerKey

    df = sqlContext.sql("SELECT app_str, pm FROM postnl_struct.srvchecks_mem")
    df_s1 = df.sample(False,0.001,25) #Sample the data
    box_prms = boxPerKey(df_s1)
    box_prms.show()
