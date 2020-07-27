# import pandas as pd
# import numpy as np
import csv, os, datetime
import shutil

from dotenv import load_dotenv
load_dotenv()

sourcePathPrefix=os.getenv('SOURCE_PREFIX', '/home/Data')
sourcePathSuffix=os.getenv('SOURCE_SUFFIX', '/data')
destPathPrefix=os.getenv('DEST_PREFIX', '/home/dest')

starttime=datetime.datetime(2019,9,17,0,0)
endtime=datetime.datetime(2020,5,12,0,0)
sensorIdx=1
sensorMap={}
d=starttime

while d<= endtime:
    print(d)
    try:
        path=os.path.join(sourcePathPrefix, d.strftime("%Y/%m/%d"), sourcePathSuffix)
        for filename in sorted(os.listdir(path)):
            sensorId = filename.split("_")[0]
            if sensorId not in sensorMap:
                sensorMap[sensorId] = 'R%s'%sensorIdx
                sensorIdx+=1
            idx = sensorMap[sensorId]
            # print(sensorId, idx)

            destDirectory = "data/%s"%(idx)

            if not os.path.exists(destDirectory):
                os.mkdir(destDirectory)

            shutil.copyfile(os.path.join(path,filename), os.path.join(destDirectory, filename.split("_")[1]))
    except Exception as e:
        print(e)
    # print(path)
    d += datetime.timedelta(days=1)

