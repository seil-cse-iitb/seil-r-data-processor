# import pandas as pd
# import numpy as np
import csv, os, datetime, json
import shutil

from dotenv import load_dotenv
load_dotenv()

sourcePathPrefix=os.getenv('SOURCE_PREFIX', '/home/Data')
sourcePathSuffix=os.getenv('SOURCE_SUFFIX', '/data')
destPathPrefix=os.getenv('DEST_PREFIX', '/home/dest')
startDateStr = os.getenv('START_DATE', '2019-01-31')
endDateStr = os.getenv('END_DATE', '2019-12-31')

startDate=datetime.strptime(startDateStr, '%Y-%m-%d')
endDate=datetime.strptime(endDateStr, '%Y-%m-%d')
sensorIdx=1
sensorMap={}
d=startDate

# First we need to get a list of all the sensors
# Iterate through the list of dates
while d<= endDate:
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

# Now that we have the sensor map, we can iterate through the data and check for presence of files
analysis = pd.DataFrame()

# Create a list of dates. To be used by the pandas DataFrame
delta = endDate-startDate
delta = delta.days
dateList = [startDate + datetime.timedelta(days=x) for x in range(delta)]

dateList = list(map(lambda x:x.strftime('%Y-%m-%d'), dateList))
# Create a column with the list of dates
analysis['date'] = dateList

# Iterate through the sensor map
for sensor in sensorMap:
    print(sensor)
    # directory = "data/%s"%sensor
    availabilityList=[]
    for date in dateList:
        # Generate the directory path
        path=os.path.join(sourcePathPrefix, d.strftime("%Y/%m/%d"), sourcePathSuffix)

        # The file could be a csv or compressed csv (csv.gz)
        filename1 = '%s_%s.csv'%(date, sensor)
        filename1 = os.path.join(path, filename1)
        filename2 = '%s_%s.csv.gz'%(date, sensor)
        filename2 = os.path.join(path, filename2)
        
        try:
            # Check if either file exists then insert a 1 to availability list
            if os.path.isfile(filename1) or os.path.isfile(filename2):
                availabilityList.append(str(1))
            else:
                # If either file doesn't exist, insert a 0
                availabilityList.append(str(0))
        except Exception as  e:
            # If anything should go wrong while reading file, insert a 0
            print(e)
            availabilityList.append(str(0))

    # Insert availability data into analysis df
    analysis[sensor]=availabilityList

# Save the dataframe as a csv
analysis.to_csv('analysis.csv', index=False)
# print(analysis)
