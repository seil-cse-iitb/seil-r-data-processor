# import pandas as pd
# import numpy as np
import csv, os, datetime
import shutil

from dotenv import load_dotenv
load_dotenv()

sourcePathPrefix=os.getenv('SOURCE_PREFIX', '/home/Data')
sourcePathSuffix=os.getenv('SOURCE_SUFFIX', '/data')
destPathPrefix=os.getenv('DEST_PREFIX', '/home/dest')

startDateStr = os.getenv('START_DATE', '2019-01-31')
endDateStr = os.getenv('END_DATE', '2019-12-31')

startDate=datetime.datetime.strptime(startDateStr, '%Y-%m-%d')
endDate=datetime.datetime.strptime(endDateStr, '%Y-%m-%d')

sensorList = os.getenv('SENSOR_LIST',"")
sensorList = sensorList.split(",")
if sensorList[0] == '':
    sensorList = None
print(sensorList)
sensorIdx=1
sensorMap={}
d=startDate

while d<= endDate:
    print(d)
    try:
        path=os.path.join(sourcePathPrefix, d.strftime("%Y/%m/%d"), sourcePathSuffix)
        for filename in sorted(os.listdir(path)):
            sensorId = filename.split("_")[0]
            if sensorList and sensorId not in sensorList:
                continue
            print("Copying %s"%filename)
            #if sensorId not in sensorMap:
            #    sensorMap[sensorId] = 'R%s'%sensorIdx
            #    sensorIdx+=1
            #idx = sensorMap[sensorId]
            # print(sensorId, idx)

            destDirectory = os.path.join(destPathPrefix,"%s"%(sensorId))

            if not os.path.exists(destDirectory):
                os.mkdir(destDirectory)
            try:
                shutil.copyfile(os.path.join(path,filename), os.path.join(destDirectory, filename.split("_")[1]))
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)
    # print(path)
    d += datetime.timedelta(days=1)

