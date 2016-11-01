#!/bin/python

from pyspark import SparkContext
from pyspark.streaming import StreamingContext



# Function to create and setup a new StreamingContext
def functionToCreateContext():
    sc = SparkContext(...)   # new context
    ssc = new StreamingContext(...)
    lines = ssc.socketTextStream(...) # create DStreams
    ...
    ssc.checkpoint(checkpointDirectory)   # set checkpoint directory
    return ssc


# Create a local StreamingContext with two working thread and batch interval of 1 second
sc = SparkContext("local[2]", "NetworkWordCount")
ssc = StreamingContext(sc, 1)

#Reduce logging to only errors
sc.setLogLevel('WARN')

# Create a DStream that will connect to hostname:port, like localhost:9999
lines = ssc.socketTextStream("localhost", 9999)

# Split each line into words
words = lines.flatMap(lambda line: line.split(" "))

#Count each word in each batch
pairs = words.map(lambda word: (word, 1))
wordCountsWind = pairs.reduceByKeyAndWindow(lambda x, y: x + y,lambda x, y: x -y,30,10)


# Print the first ten elements of each RDD generated in this DStream to the console
wordCountsWind.pprint()

ssc.start()             # Start the computation
ssc.awaitTermination()  # Wait for the computation to terminate
