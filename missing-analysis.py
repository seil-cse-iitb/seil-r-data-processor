import pandas as pd
import numpy as np
import csv, os, datetime

sensorIdx=1
analysis = pd.DataFrame()

# Very hacky method to get list of all dates
startdate = datetime.datetime(2019,7,17,0,0)
enddate = datetime.datetime(2020,5,9,0,0)
delta = enddate-startdate
delta = delta.days
dateList = [startdate + datetime.timedelta(days=x) for x in range(delta)]

dateList = list(map(lambda x:x.strftime('%Y-%m-%d'), dateList))

# dateList =  sorted(os.listdir("data/R1"))
# dateList = list(map(lambda x:x.split(".")[0], dateList))

analysis['date'] = dateList

for sensor in sorted(os.listdir("data")):
    print(sensor)
    directory = "data/%s"%sensor
    availabilityList=[]
    for date in dateList:
        # print(os.path.join(directory, filename))        
        filename = '%s.csv'%date
        # print(date)
        try:
            df = pd.read_csv(os.path.join(directory, filename), header=None, usecols=[3])  
            lines = len(df)
            df = df.diff()
            freq = round(int(df.median()))
            # print(freq)
            expectedLines = 3600*24/freq
            availabilityList.append(str( min(lines/expectedLines,1) ))
        except Exception as  e:
            # print(e)
            availabilityList.append(str(0))

    # Insert availability data into analysis df
    analysis[sensor]=availabilityList
analysis.to_csv('analysis.csv', index=False)
print(analysis)
