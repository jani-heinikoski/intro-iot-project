import os
import pandas as pd
from influxdb_client_3 import InfluxDBClient3, Point, WritePrecision
import pyarrow

TOKEN = os.getenv('INFLUXDB_TOKEN')
ORG = os.getenv('INFLUXDB_ORG')
HOST = os.getenv('INFLUXDB_HOST')
BUCKET = 'environment'
MEASUREMENT = 'env_data'

if (TOKEN == None or ORG == None or HOST == None):
    print('Please set the required environment variables to connect to the InfluxDB database.')
    exit(-1)

client = InfluxDBClient3(token=TOKEN,
                         host=HOST,
                         org=ORG,
                         database=BUCKET)

ex_ts = pd.Timestamp.now(tz="Europe/Helsinki") - pd.Timedelta(days=29)
point = Point(MEASUREMENT).tag("sensor", "linux-ubuntu-vm").field("temperature", float(23.5)).time(time=ex_ts, write_precision=WritePrecision.S)

client.write(point)

query = 'select * from %s' % (MEASUREMENT)
df: pd.DataFrame = client.query(query=query, language="sql").to_pandas()
print(df.head(), end='\n\n\n')
print(df.info())