# meteoblue Python Dataset SDK

[![PyPI version](https://badge.fury.io/py/meteoblue-dataset-sdk.svg)](https://badge.fury.io/py/meteoblue-dataset-sdk)

This library simplifies access to the [meteoblue dataset API](https://docs.meteoblue.com/en/apis/environmental-data/dataset-api).

In order to use this library you need a meteoblue API key.

Features:
- Fetch any dataset from the meteoblue environmental data archive
- Transparently integrates job queues to query large datasets
- Efficiently transfers data using compressed protobuf messages
- Asynchronous interface to query data in parallel
- Data can be used as simple floating-point arrays. No further formatting required.
- Semantic Versioning: The interface for version 1 is declared stable. Breaking interface changes will be published in version 2.

Example notebooks:
- [Basic example](https://github.com/meteoblue/python-dataset-sdk/blob/master/example.ipynb)
- [Using model data, creating graphs and maps](https://github.com/meteoblue/python-dataset-sdk/blob/master/example_datasets.ipynb)
- [Using measurement data](https://github.com/meteoblue/python-dataset-sdk/blob/master/example_measurements.ipynb)
## Installation
- Ensure that you are using at least Python 3.7 with `python --version` (Sometimes `python3`)
- Install the module with `pip install 'meteoblue_dataset_sdk >=1.0,<2.0'` (Sometimes `pip3`)

This module will also install the following dependencies automatically:
- aiohttp >=3.9,<4
- protobuf >=5.0,<6
- aiofiles >=24.1.0,<25


## Usage
See [main.py](https://github.com/meteoblue/python-dataset-sdk/blob/master/main.py) for a working example. To generate the query JSON it is highly recommended to use the [dataset API web interfaces](https://docs.meteoblue.com/en/apis/environmental-data/web-interfaces).

```python
import meteoblue_dataset_sdk
import logging

# Display information about the current download state
logging.basicConfig(level=logging.INFO)

query = {
    "units": {
        "temperature": "C",
        "velocity": "km/h",
        "length": "metric",
        "energy": "watts",
    },
    "geometry": {
        "type": "MultiPoint",
        "coordinates": [[7.57327, 47.558399, 279]],
        "locationNames": ["Basel"],
    },
    "format": "protobuf",
    "timeIntervals": ["2019-01-01T+04:00/2019-01-01T+04:00"],
    "timeIntervalsAlignment": "none",
    "queries": [
        {
            "domain": "NEMSGLOBAL",
            "gapFillDomain": None,
            "timeResolution": "hourly",
            "codes": [{"code": 11, "level": "2 m above gnd"}],
        }
    ],
}
client = meteoblue_dataset_sdk.Client(apikey="xxxxxx")
result = client.query_sync(query)
# result is a structured object containing timestamps and data

timeInterval = result.geometries[0].timeIntervals[0]
data = result.geometries[0].codes[0].timeIntervals[0].data

print(timeInterval)
# start: 1546286400
# end: 1546372800
# stride: 3600
```
NOTE: a UTC offset can be specified in the time interval (in the example: `+04:00`)

NOTE: `timeInterval.end` is the first timestamp that is not included anymore in the time interval.

If your code is using `async/await`, you should use `await client.query()` instead of `client.query_sync()`. Asynchronous IO is essential for modern webserver frameworks like Flask or FastAPI.

```python
client = meteoblue_dataset_sdk.Client(apikey="xxxxxx")
result = await client.query(query)
```

## Caching results
If you are training a model and re-run your program multiple times, you can enable caching to store results from the meteoblue dataset SDK on disk. A simple file cache can be enabled with:

```python
import zlib
from meteoblue_dataset_sdk.caching import FileCache

# Cache results for 1 day (86400 seconds)
cache = FileCache(path="./mb_cache", max_age=86400, compression_level=zlib.Z_BEST_SPEED)
client = meteoblue_dataset_sdk.Client(apikey="xxxxxx", cache=cache)
```

If you want to implement a different cache (e.g. redis or S3), the SDK offers an abstract base class `caching.cache.AbstractCache`. The required methods are listed [here](https://github.com/meteoblue/python-dataset-sdk/blob/master/meteoblue_dataset_sdk/caching/abstractcache.py).


## Working with timestamps
Time intervals are encoded as a simple `start`, `end` and `stride` unix timestamps. With just a  view lines of code, timestamps can be converted to an array of datetime objects:

```python
import datetime as dt

print(timeInterval)
# start: 1546286400
# end: 1546372800
# stride: 3600

timerange = range(timeInterval.start, timeInterval.end, timeInterval.stride)
timestamps = list(map(lambda t: dt.datetime.fromtimestamp(t, dt.timezone.utc), timerange))
```

This code works well for regular timesteps like hourly, 3-hourly or daily data. Monthly data is unfortunately not regular, and the API returns timestamps as an string array. The following code takes care of all cases and always returns an array of datetime objects. Note that a timezone object different from UTC can be specified to e.g. match the utc offset of the request:

```python
import datetime as dt
import dateutil.parser

def meteoblue_timeinterval_to_timestamps(t, timezone = dt.timezone.utc):
    if len(t.timestrings) > 0:
        def map_ts(time):
            if "-" in time:
                return dateutil.parser.parse(time.partition("-")[0])
            return dateutil.parser.parse(time)

        return list(map(map_ts, t.timestrings))

    timerange = range(t.start, t.end, t.stride)
    return list(map(lambda t: dt.datetime.fromtimestamp(t, timezone), timerange))

query = { ... }
result = client.query_sync(query)
timestamps_utc = meteoblue_timeinterval_to_timestamps(timeInterval)
print(timestamps_utc)
# [datetime.datetime(2018, 12, 31, 20, 0, tzinfo=datetime.timezone.utc),
#  datetime.datetime(2018, 12, 31, 21, 0, tzinfo=datetime.timezone.utc),
#  ...]


timezone = dt.timezone(dt.timedelta(hours=4))
timestamps = meteoblue_timeinterval_to_timestamps(timeInterval, timezone)
print(timestamps)
# [datetime.datetime(2019, 1, 1, 0, 0, tzinfo=datetime.timezone(datetime.timedelta(seconds=14400))),
#  datetime.datetime(2019, 1, 1, 1, 0, tzinfo=datetime.timezone(datetime.timedelta(seconds=14400))),
#  ...]
```

## Working with dataframes
To convert a result from the meteoblue dataset API to pandas dataframe, a few lines of code can help:

```python
import pandas as pd
import numpy as np

def meteoblue_result_to_dataframe(geometry):
    t = geometry.timeIntervals[0]
    timestamps = meteoblue_timeinterval_to_timestamps(t)

    n_locations = len(geometry.lats)
    n_timesteps = len(timestamps)

    df = pd.DataFrame(
        {
            "TIMESTAMP": np.tile(timestamps, n_locations),
            "Longitude": np.repeat(geometry.lons, n_timesteps),
            "Latitude": np.repeat(geometry.lats, n_timesteps),
        }
    )

    for code in geometry.codes:
        name = str(code.code) + "_" + code.level + "_" + code.aggregation
        df[name] = list(code.timeIntervals[0].data)

    return df

query = { ... }
result = client.query_sync(query)
df = meteoblue_result_to_dataframe(result.geometries[0])
```

## Protobuf format
In the background, data is transferred using protobuf and defined as [this protobuf structure](https://github.com/meteoblue/python-dataset-sdk/blob/master/meteoblue_dataset_sdk/protobuf/dataset.proto).

A 10 year hourly data series for 1 location requires `350 kb` using protobuf, compared to `1600 kb` using JSON. Additionally the meteoblue Python SDK transfers data using gzip which reduces the size to only `87 kb`.

More detailed output of the `result` protobuf object:

```
geometries {
  domain: "NEMSGLOBAL"
  lats: 47.6665192
  lons: 7.5
  asls: 499.773651
  locationNames: "Basel"
  nx: 1
  ny: 1
  timeResolution: "hourly"
  timeIntervals {
    start: 1546286400
    end: 1546372800
    stride: 3600
  }
  codes {
    code: 11
    level: "2 m above gnd"
    unit: "°C"
    aggregation: "none"
    timeIntervals {
      data: 3.51
      data: 3.4
      data: 3.22
      data: 3.02
      data: 2.89
      data: 2.69
      data: 2.55
      data: 2.38
      data: 2.27
      data: 2.12
      data: 1.99
      data: 1.83
      data: 1.82
      data: 2.1
      data: 2.43
      data: 2.92
      data: 3.72
      data: 3.93
      data: 3.91
      data: 3.53
      data: 3.13
      data: 2.88
      data: 2.65
      data: 2.46
    }
  }
}
```
