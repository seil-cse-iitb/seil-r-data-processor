import pandas as pd
import numpy as np
import csv, os, datetime, json
import shutil

from dotenv import load_dotenv
load_dotenv()

sourceDir = os.getenv("SOURCE_DIR","data.old")
destDir = os.getenv("DEST_DIR","data-processed")

# Each sensor is in its own sourceDir inside data
# We need to iterate through each
for sensorId in sorted(os.listdir(sourceDir)):
    # Now we need to open each file inside this sourceDir
    for filename in os.listdir(os.path.join(sourceDir, sensorId)):
        print("%s/%s/%s"%(sourceDir,sensorId, filename))

        # This line performs the stripping by setting the usecols parameter to those we need
        # Each file contain 20 fields- Timestamp (TS), voltage (V1/V2/V3), current (A1/A2/A3), 
        # active power (W1/W2/W3), re-active power (VAR1/VAR2/VAR3), power factor (PF1/PF2/PF3),
        # angle (Ang1/Ang2/Ang3) for phase𝜙1/𝜙2/𝜙3 respectively and frequency (F).
        try:
            df = pd.read_csv(os.path.join("%s/%s"%(sourceDir,sensorId), filename), header=None, 
            usecols=[3, 4,5,6, 7,8,9, 10,11,12, 16,17,18, 19,20,21, 22,23,27,  42 ],
            names=["TS", "V1","V2","V3", "A1","A2","A3", "W1","W2","W3", "VAR1","VAR2","VAR3", "PF1","PF2","PF3", "Ang1","Ang2","Ang3", "F"])
            
            # We want to save the processed files in a separate directory
            # If it doesnt exist we need to create it
            if not os.path.exists("%s/%s"%(destDir, sensorId)):
                os.mkdir("%s/%s"%(destDir, sensorId))
            df.to_csv(os.path.join("%s/%s"%(destDir,sensorId), filename), index=False)
        except Exception as e:
            print(e)
# import pandas as pd
# import numpy as np
# import csv, os, datetime, json
# df = pd.read_csv(os.path.join("data.old/", "R1/2019-07-18.csv"), header=None, 
#         usecols=[3, 4,5,6, 7,8,9, 10,11,12, 16,17,18, 19,20,21, 22,23,27,  42 ],
#         names=["TS", "V1","V2","V3", "A1","A2","A3", "W1","W2","W3", "VAR1","VAR2","VAR3", "PF1","PF2","PF3", "Ang1","Ang2","Ang3", "F"])

# df.to_csv(os.path.join("data.old/", "R1/2019-07-17.csv"), index=False)