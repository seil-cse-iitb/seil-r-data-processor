import dask
import dask.dataframe as dd
from dask.array import stats
import pandas as pd
import os

def process(sensorId):
    print("Processing %s"%sensorId)
    df = dd.read_csv('data-processed/%s/*.csv'%(sensorId), usecols=["W1","W2","W3"])
    x = (df.W1.abs() + df.W2.abs() + df.W3.abs())
    m, std, kurtosis, skew, minimum, maximum = [x.mean(), x.std(), stats.kurtosis(x), stats.skew(x), x.min(), x.max()]
    result = dask.compute(m, std, kurtosis, skew, minimum, maximum)
    print(result)
    return result

def findNaN(sensorId):
    print("Processing %s"%sensorId)
    for filename in os.listdir("data-processed/%s"%sensorId):
        df = pd.read_csv('data-processed/%s/%s'%(sensorId, filename), usecols=["W1","W2","W3"])
        if df.isnull().values.any():
            print("Found nan in %s/%s"%(sensorId, filename))

with open("stats.csv", 'w') as f:
    f.write("sensorId, mean, standard deviation, kurtosis, skew, minimum, maximum\n")

for sensorId in sorted(os.listdir("data-processed")):
    result = process(sensorId)

    with open("stats.csv", 'a') as f:
        f.write("%s,%f,%f,%f,%s,%f,%f\n"%(sensorId, result[0], result[1], result[2], result[3], result[4], result[5]))

# process("1")