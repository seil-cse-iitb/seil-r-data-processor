import pandas as pd
import numpy as np
import csv, os, datetime

from dotenv import load_dotenv
load_dotenv()

sourcePathPrefix=os.getenv('SOURCE_PREFIX', '/home/Data')
sourcePathSuffix=os.getenv('SOURCE_SUFFIX', '/data')
destPathPrefix=os.getenv('DEST_PREFIX', '/home/dest')

starttime=datetime.datetime(2019,7,17,0,0).timestamp()
increment = 24*3600
endtime=datetime.datetime(2020,5,12,0,0).timestamp()
sensorIdx=1
sensorMap={}
d=datetime.datetime.fromtimestamp(starttime)

path=os.path.join(sourcePathPrefix, d.strftime("%Y/%m/%d"), sourcePathSuffix)
for filename in os.listdir(path):
    sensorId = filename.split("_")[0]
    if sensorId in sensorMap:
        idx = sensorMap[sensorId]
    else:
        sensorMap[sensorId] = sensorIdx
        sensorIdx+=1
    print(id)
print(path)

