import pandas as pd
import numpy as np
import csv, os, datetime
from dotenv import load_dotenv
load_dotenv()
sensorIdx=1
analysis = pd.DataFrame()

# Very hacky method to get list of all dates
startDateStr = os.getenv('START_DATE', '2019-01-31')
endDateStr = os.getenv('END_DATE', '2019-12-31')

startDate=datetime.datetime.strptime(startDateStr, '%Y-%m-%d')
endDate=datetime.datetime.strptime(endDateStr, '%Y-%m-%d')
delta = endDate-startDate
delta = delta.days
dateList = [startDate + datetime.timedelta(days=x) for x in range(delta)]

dateListStr = list(map(lambda x:x.strftime('%Y-%m-%d'), dateList))
# Create a column with the list of dates
analysis['date'] = dateListStr

# Iterate through each sensorId directory in data
for sensorId in sorted(os.listdir("data")):
    print(sensorId)
    # We need to enter each directory
    directory = "data/%s"%sensorId
    availabilityList=[]

    # Now we need to go through each file in the directory by date
    for date in dateList:
        # Construct the filename
        filename = '%s.csv'%(date.strftime('%Y-%m-%d'))
        filename = os.path.join(directory, filename)
        print(filename)
        try:
            # Check if either file exists then insert a 1 to availability list
            if os.path.isfile(filename):
                availabilityList.append(str(1))
            else:
                # If either file doesn't exist, insert a 0
                availabilityList.append(str(0))
        except Exception as  e:
            # If anything should go wrong while reading file, insert a 0
            print(e)
            availabilityList.append(str(0))

        # try:
        #     df = pd.read_csv(os.path.join(directory, filename), header=None, usecols=[3])  
        #     lines = len(df)
        #     df = df.diff()
        #     freq = round(int(df.median()))
        #     # print(freq)
        #     expectedLines = 3600*24/freq
        #     availabilityList.append(str( min(lines/expectedLines,1) ))
        # except Exception as  e:
        #     # print(e)
        #     availabilityList.append(str(0))

    # Insert availability data into analysis df
    analysis[sensorId]=availabilityList
analysis.to_csv('analysis.csv', index=False)
print(analysis)
