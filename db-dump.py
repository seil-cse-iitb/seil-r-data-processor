import MySQLdb as dbapi
import sys, os, datetime, csv
from dotenv import load_dotenv
load_dotenv()

dbHost=os.getenv('DB_HOST','localhost')
dbUser=os.getenv('DB_USER','torvalds')
dbPass=os.getenv('DB_PASSWORD','showmethecode')
dbName=os.getenv('DB_NAME','sensor_db')
tableName=os.getenv('TABLE_NAME', 'power_meters')
DAYS_TO_FETCH=3
def getQueryResults(queryString):

    db=dbapi.connect(host=dbHost,user=dbUser,passwd=dbPass, database=dbName)
    cur=db.cursor()
    print("Running query %s"%queryString)
    cur.execute(queryString)

    rows = cur.fetchall()
    return rows

def saveToCsv(rows, filename):
    fp = open(filename, 'w')
    myFile = csv.writer(fp)
    print("Saving to CSV")
    myFile.writerows(rows)
    fp.close()

# Get list of sensors
queryString ='SELECT distinct sensor_id FROM %s order by sensor_id;'%tableName
rows = getQueryResults(queryString)
saveToCsv(rows, 'sensors.csv')
sensors = list(rows)

# Fetch measurements of R1 for one day and save to csv
sensorIdx=0
increment = 24*3600
starttime=datetime.datetime(2017,1,1,0,0).timestamp()
for i in range(1,DAYS_TO_FETCH+1):
    endtime=starttime+increment
    queryString ='''SELECT  TS, V1, V2, V3, A1, A2, A3, W1, W2, W3, VAR1, VAR2, VAR3, PF1, PF2, PF3, Ang1, Ang2, Ang3, F
                    FROM %s where sensor_id="%s" and TS >=%s and TS<%s;'''%(tableName, sensors[sensorIdx][0], starttime, endtime)
    rows = getQueryResults(queryString)
    d=datetime.datetime.fromtimestamp(starttime)
    directory = "data/R%d"%(sensorIdx+1)
    print('Saving %s/%s-%s-%s.csv'%(directory,d.year,d.month,d.day))
    if not os.path.exists(directory):
        os.mkdir(directory)
    saveToCsv(rows, '%s/%s-%s-%s.csv'%(directory,d.year,d.month,d.day))

    # increment starttime
    starttime += increment
