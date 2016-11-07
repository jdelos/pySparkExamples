#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""
pySpark example how to use the boxParms spark module

In this case we generate the boxParmas for a sample data to make it run fast.

Run this example by executing this line:
    spark-commit pySpark_genBoxPrms.py

@author: julia.delos
"""

from __future__ import print_function
from pyspark import SparkContext, HiveContext

if __name__ == "__main__":
    print("Creating spark context")
    sc = SparkContext(master="yarn-client",appName="PythonStreamingWindowedWC_Cluster")
    sqlContext = HiveContext(sc)
    sc.setLogLevel('ERROR')

    #Add python module
    sc.addPyFile('boxParms.py')
    from boxParms import boxPerKey

    df = sqlContext.sql("SELECT app_str, pm FROM postnl_struct.srvchecks_mem")
    df_s1 = df.sample(False,0.001,25) #Sample the data
    box_prms = boxPerKey(df_s1,0,1)
    box_prms.show()


