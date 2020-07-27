import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('analysis.csv')
dates = list(df['date'])
sensors = list(df)[1:]
availability = df
del availability['date']
availability = availability.clip(0,1)
availability = availability.transpose()
print(availability)

fig, ax = plt.subplots()
im = ax.imshow(availability)

# We want to show all ticks...
# ax.set_xticks(np.arange(len(dates)))
ax.set_yticks(np.arange(len(sensors)))
# ... and label them with the respective list entries
# ax.set_xticklabels(dates)
ax.set_yticklabels(sensors)

# Rotate the tick labels and set their alignment.
# plt.setp(ax.get_xticklabels(), rotation=45, ha="right",rotation_mode="anchor")

ax.set_title("Availability of sensor data in 2019-20")
# fig.tight_layout()
fig.set_size_inches(50, 10)
plt.colorbar(im)
plt.savefig("availability.png")
