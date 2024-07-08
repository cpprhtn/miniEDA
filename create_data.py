import pandas as pd
import numpy as np
import datetime

# setting
num_devices = 5
start_date = datetime.datetime(2024, 1, 1, 0, 0, 0)
end_date = datetime.datetime(2024, 1, 2, 0, 0, 0)
time_delta = datetime.timedelta(minutes=1)

timestamps = []
device_ids = []
power_consumptions = []

current_time = start_date
while current_time < end_date:
    for device_id in range(1, num_devices + 1):
        timestamps.append(current_time)
        device_ids.append(device_id)
        power_consumptions.append(round(np.random.normal(loc=20.0, scale=5.0), 2))
    current_time += time_delta

data = pd.DataFrame({
    'timestamp': timestamps,
    'device_id': device_ids,
    'power_consumption': power_consumptions
})

data.to_csv('power_consumption_example.csv', index=False)
