import os
import pandas as pd
from influxdb_client_3 import InfluxDBClient3, Point, WritePrecision

TOKEN = os.getenv('INFLUXDB_TOKEN')
ORG = os.getenv('INFLUXDB_ORG')
HOST = os.getenv('INFLUXDB_HOST')
BUCKET = 'environment'
MEASUREMENT = 'env_data'
TZ = 'Europe/Helsinki'

if (TOKEN == None or ORG == None or HOST == None):
    print('Please set the required environment variables to connect to the InfluxDB database.')
    exit(-1)

client = InfluxDBClient3(token=TOKEN,
                         host=HOST,
                         org=ORG,
                         database=BUCKET)

# Example timestamp from 29 days ago (Helsinki timezone)
ex_ts = pd.Timestamp.now(tz=TZ) - pd.Timedelta(days=29)
point = Point(MEASUREMENT).tag("sensor", "linux-ubuntu-vm").field("temperature", float(23.5)).time(time=ex_ts, write_precision=WritePrecision.S)

client.write(point)

query = 'select * from %s' % (MEASUREMENT)
df: pd.DataFrame = client.query(query=query, language="sql").to_pandas()
# Localize the times back to Helsinki timezone
df['time'] = df['time'].dt.tz_localize(TZ)
print(df.head(100), end='\n\n\n')
print(df.info())