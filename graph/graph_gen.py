import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from influxdb_client_3 import InfluxDBClient3, flight_client_options

import certifi

# Environment variables for connecting to the InfluxDB database
TOKEN = os.getenv('INFLUXDB_TOKEN')
ORG = os.getenv('INFLUXDB_ORG')
HOST = os.getenv('INFLUXDB_HOST')

BUCKET = 'environment'

fh = open(certifi.where(), "r")
cert = fh.read()
fh.close()

def get_data(client, query):
    data: pd.DataFrame = client.query(query).to_pandas()
    data = data.drop("sensor", axis=1)
    data = data.set_index("time")
    return data
    
def setup_subplot(data, title: str, ylabel: str, color: str ='blue', grid: bool = "true", marker=" ", style: str = "-", mean: bool = False):
    fig, ax = plt.subplots(figsize=(16, 6))
    ax.plot(data,color=color, linestyle=style, marker=marker)
    ax.set_title(title) 
    ax.set_ylabel(ylabel)

    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d.%m.%y"))

    # Calculate mean value
    if (mean):
        ax.axhline(y=np.nanmean(data), color="red")
    ax.grid(grid)
    return fig, ax

def convert_to_bin(data, key, threshold):
    data[key] = [1 if el < threshold else 0 for el in data[key].values]
    return data

def main():
    # Connect to db
    client = InfluxDBClient3(token=TOKEN, host=HOST, org=ORG, database=BUCKET, flight_client_options=flight_client_options(tls_root_certs=cert))
    data = get_data(client, "SELECT * FROM sample_env_data ORDER BY time ASC")

    # Draw graphs
    setup_subplot(data["humidity"], "Air humidity 5.11.2023 - 12.11.2023", "Air humidity (%)")
    setup_subplot(data["pressure"], "Air pressure 5.11.2023 - 12.11.2023", "Air pressure (mBar)")
    setup_subplot(data["temperature"], "Air temperature 5.11.2023 - 12.11.2023", "Air temperature (°C)", mean=True)

    # Draw binary graph
    bin_data = convert_to_bin(data, "temperature", 3)
    setup_subplot(bin_data["temperature"], "Air temperatures below 3°C 5.11.2023 - 12.11.2023", "Air temperature (°C)", marker=".", style=" ", color="black")
    plt.show()

if __name__ == '__main__':
    main()