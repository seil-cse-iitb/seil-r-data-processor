# Getting Started

* Create a virtual environment
```
virtualenv -p python3 .seil-r.venv
```

* Activate the virtual environment
```
source .seil-r.venv/bin/activate
```

* Install python dependencies
```
pip install -r requirements.txt
```

# Scripts

* To plot the missing analysis, set the START_DATE and END_DATE in `.env` and run 
```
python plot.py
```
It will generate an image with the naming convention `availabilitiy-START_DATE-to-END_DATE.png`

* The raw files contained more fields than necessary, so we strip them out
```
python strip-columns.py
```

* Generate useful statistics like mean, standard deviation, kurtosis, skew, etc.
```
python statistics.py
```
We make use of Dask to perform analysis on multiple csv files without loading them all into memory
This needs Python 3.6 which is not installed by default on Ubuntu 16.