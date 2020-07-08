import pandas as pd
import numpy as np
import csv, os

sensorIdx=1
analysis = pd.DataFrame()

# Very hacky method to get list of all dates
dateList =  sorted(os.listdir("data/R1"))
dateList = list(map(lambda x:x.split(".")[0], dateList))

analysis['date'] = dateList

for sensor in os.listdir("data"):
    directory = "data/%s"%sensor
    availabilityList=[]
    for filename in sorted(os.listdir(directory)):
        if filename.endswith(".csv"):
             # print(os.path.join(directory, filename))        
            date = filename.split(".")[0]
            # print(date)
            try:
                df = pd.read_csv(os.path.join(directory, filename), header=None, usecols=[0])  
                df = df.diff()
                lines = len(df)
                freq = round(df.mode()[0][0])
                expectedLines = 3600*24/freq
                availabilityList.append(str(lines/expectedLines))
            except Exception as  e:
                availabilityList.append(str(0))

    # Insert availability data into analysis df
    analysis[sensor]=availabilityList
analysis.to_csv('analysis.csv', index=False)
print(analysis)
