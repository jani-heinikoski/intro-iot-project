# Authors: Jani Heinikoski, Vili Huusko
# Sources:
# - https://github.com/InfluxCommunity/influxdb3-python
# - https://pandas.pydata.org/docs/
# - https://pythonhosted.org/sense-hat/api/

import os
import pandas as pd
import random
from typing import List, Dict
from influxdb_client_3 import InfluxDBClient3, Point, WritePrecision
from sense_emu import SenseHat

# Environment variables for connecting to the InfluxDB database
TOKEN = os.getenv('INFLUXDB_TOKEN')
ORG = os.getenv('INFLUXDB_ORG')
HOST = os.getenv('INFLUXDB_HOST')
# Global variables, can change as per needed
BUCKET = 'environment'
MEASUREMENT = 'sample_env_data'
SENSOR_TAG = 'linux-ubuntu-vm'
TZ = 'Europe/Helsinki'


def read_measurement(sense: SenseHat) -> Dict[str, float]:
    return {
        "temperature": float(sense.get_temperature()),
        "pressure": float(sense.get_pressure()),
        "humidity": float(sense.get_humidity())
    }


def introduce_randomness(measurement: Dict[str, float], tmp_rng_boundary: float) -> None:
    r = lambda b : random.uniform(-b, b) * random.random()
    measurement["temperature"] = measurement["temperature"] + random.uniform(-tmp_rng_boundary, -tmp_rng_boundary + 0.6)
    measurement["pressure"] = measurement["pressure"] + r(20)
    measurement["humidity"] = measurement["humidity"] + r(2)


def generate_example_data(start: pd.Timestamp, end: pd.Timestamp, freq: str, sense: SenseHat) -> List[Point]:
    points: List[Point] = []
    dt_range = pd.date_range(start=start, end=end, freq=freq, tz=TZ)
    tmp_rng_boundary = 0

    for dt in dt_range:
        # read a measurement from the Sense HAT emulator
        m = read_measurement(sense)
        tmp_rng_boundary = tmp_rng_boundary + 5 / dt_range.size

        # make night time temperatures colder than daytime
        if (dt.time().hour >= 18 and dt.time().hour <= 23):
            introduce_randomness(m, tmp_rng_boundary + (dt.time().hour / 23) / 2)
        elif (dt.time().hour >= 0 and dt.time().hour <= 6):
            introduce_randomness(m, tmp_rng_boundary + ((23 - dt.time().hour) / 23) / 2)
        else:
            introduce_randomness(m, tmp_rng_boundary)
        
        # create the data point based on the measurement from the Sense HAT emulator
        point = Point(MEASUREMENT).tag("sensor", SENSOR_TAG) \
        .field("temperature", m["temperature"]) \
        .field("pressure", m["pressure"]) \
        .field("humidity", m["humidity"]) \
        .time(time=dt, write_precision=WritePrecision.S)
        # add the data point to the list
        points.append(point)
        
    return points


def are_env_variables_set() -> bool:
    return not (TOKEN == None or ORG == None or HOST == None)


def main() -> None:
    # Check the environment variables required for creating the InfluxDB client object
    if (not are_env_variables_set()):
        print('Please set the required environment variables to connect to the InfluxDB database.')
        exit(-1)

    # Generate the example data
    start_dt = pd.Timestamp.now(tz=TZ) - pd.Timedelta(days=7)
    end_dt = pd.Timestamp.now(tz=TZ)
    example_data = generate_example_data(start=start_dt, end=end_dt, freq="1H", sense=SenseHat())

    # Open a connection to the database
    client = InfluxDBClient3(token=TOKEN, host=HOST, org=ORG, database=BUCKET)

    client.write(example_data)

    # Close the connection to the database
    client.close()
    

if (__name__ == '__main__'):
    main()