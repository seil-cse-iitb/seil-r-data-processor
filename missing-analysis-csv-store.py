# import pandas as pd
# import numpy as np
import csv, os, datetime
import shutil

from dotenv import load_dotenv
load_dotenv()

sourcePathPrefix=os.getenv('SOURCE_PREFIX', '/home/Data')
sourcePathSuffix=os.getenv('SOURCE_SUFFIX', '/data')
destPathPrefix=os.getenv('DEST_PREFIX', '/home/dest')

starttime=datetime.datetime(2018,1,1,0,0)
endtime=datetime.datetime(2019,12,31,0,0)
sensorIdx=1
sensorMap={}
d=starttime

# First we need to get a list of all the sensors
# Iterate through the list of dates
while d<= endtime:
    print(d)
    try:
        # Create the path to the data directory corresponding to the current date
        path=os.path.join(sourcePathPrefix, d.strftime("%Y/%m/%d"), sourcePathSuffix)
        # Iterate through the files
        for filename in sorted(os.listdir(path)):
            # The filename is like 1_2019-02-02.csv or 1_2019-02-02.csv.gz, so the first part before _ is the id
            sensorId = filename.split("_")[0]
            # If the sensor id is not in the map, add it
            if sensorId not in sensorMap:
                # We create an anonymous ID R<i>
                sensorMap[sensorId] = 'R%s'%sensorIdx
                # Increment the sensorIdx to be used for anonymous id generation
                sensorIdx+=1
    except Exception as e:
        print(e)
    # print(path)
    d += datetime.timedelta(days=1)

# We should have the list of all sensors now. Let's see it and save to a file, just in case
def writeDictToFile(d, filename):
    with open(filename, 'w') as outfile:
        outfile.write(json.dumps(d, indent=4))
        
print(sensorMap)
writeDictToFile(sensorMap, 'sensor-map.json')