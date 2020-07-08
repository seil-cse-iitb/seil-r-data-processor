import MySQLdb as dbapi
import sys, os, datetime, csv
from dotenv import load_dotenv
load_dotenv()

dbHost=os.getenv('DB_HOST','localhost')
dbUser=os.getenv('DB_USER','torvalds')
dbPass=os.getenv('DB_PASSWORD','showmethecode')
dbName=os.getenv('DB_NAME','sensor_db')
tableName=os.getenv('TABLE_NAME', 'power_meters')
DAYS_TO_FETCH=int(os.getenv('DAYS_TO_FETCH', 3))
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

# Create the data directory if it doesn't exist'
if not os.path.exists('data'):
    os.mkdir('data')

# Run a loop for all sensors
for sensorIdx, sensor in enumerate(sensors):
    # Anonymise the sensor id with an index
    print("Sensor idx: "+sensorIdx)
    increment = 24*3600
    starttime=datetime.datetime(2017,1,1,0,0).timestamp()
    # Fetch measurements of R<i> for DAYS_TO_FETCH starting from 2017-01-01
    for i in range(1,DAYS_TO_FETCH+1):
        # Fetch measurements of R<i> for one day and save to csv
        endtime=starttime+increment
        queryString ='''SELECT  TS, V1, V2, V3, A1, A2, A3, W1, W2, W3, VAR1, VAR2, VAR3, PF1, PF2, PF3, Ang1, Ang2, Ang3, F
                        FROM %s where sensor_id="%s" and TS >=%s and TS<%s;'''%(tableName, sensor[0], starttime, endtime)
        # Get rows from DB
        rows = getQueryResults(queryString)
        # Convert starttime from epoch to YYYY-MM-DD format to create csv file
        d=datetime.datetime.fromtimestamp(starttime)
        directory = "data/R%d"%(sensorIdx+1)
        print('Saving %s/%s.csv'%(directory,d.strftime('%Y-%m-%d')))
        # Create the directory corresponding to R<i> if it doesn't exist'
        if not os.path.exists(directory):
            os.mkdir(directory)
        saveToCsv(rows, '%s/%s.csv'%(directory,d.strftime('%Y-%m-%d')))

        # increment starttime by one day
        starttime += increment
