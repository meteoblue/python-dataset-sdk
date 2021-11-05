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
- [Basic example](example.ipynb)
- [Creating graphs and maps](example_graphs_and_maps.ipynbs)
- [Using measurement data](example_measurements.ipynb)
## Installation
- Ensure that you are using at least Python 3.7 with `python --version` (Sometimes `python3`)
- Install the module with `pip install 'meteoblue_dataset_sdk >=1.0,<2.0'` (Sometimes `pip3`)

This module will also install the following dependencies automatically:
- aiohttp >=3.6,<4
- protobuf >=3.0,<4


## Usage
See [main.py](./main.py) for a working example. To generate the query JSON it is highly recommended to use the [dataset API web interfaces](https://docs.meteoblue.com/en/apis/environmental-data/web-interfaces).

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
    "timeIntervals": ["2019-01-01T+00:00/2019-01-01T+00:00"],
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
# start: 1546300800
# end: 1546387200
# stride: 3600
```

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

If you want to implement a different cache (e.g. redis or S3), the SDK offers an abstract base class `caching.cache.AbstractCache`. The required methods are listed [here](./meteoblue_dataset_sdk/caching/abstractcache.py).


## Working with timestamps
Time intervals are encoded as a simple `start`, `end` and `stride` unix timestamps. With just a  view lines of code, timestamps can be converted to an array of datetime objects:

```python
import datetime as dt

print(timeInterval)
# start: 1546300800
# end: 1546387200
# stride: 3600

timerange = range(timeInterval.start, timeInterval.end, timeInterval.stride)
timestamps = list(map(lambda t: dt.date.fromtimestamp(t), timerange))
```

This code works well for regular timesteps like hourly, 3-hourly or daily data. Monthly data is unfortunately not regular, and the API returns timestamps as an string array. The following code takes care of all cases and always returns an array of datetime objects:

```python
import datetime as dt
import dateutil.parser

def meteoblue_timeinterval_to_timestamps(t):
    if len(t.timestrings) > 0:
        def map_ts(time):
            if "-" in time:
                return dateutil.parser.parse(time.partition("-")[0])
            return dateutil.parser.parse(time)

        return list(map(map_ts, t.timestrings))

    timerange = range(t.start, t.end, t.stride)
    return list(map(lambda t: dt.datetime.fromtimestamp(t), timerange))

query = { ... }
result = client.query_sync(query)
timestamps = meteoblue_timeinterval_to_timestamps(result.geometries[0].timeIntervals[0])
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
        df[name] = code.timeIntervals[0].data

    return df

query = { ... }
result = client.query_sync(query)
df = meteoblue_result_to_dataframe(result.geometries[0])
```

## Protobuf format
In the background, data is transferred using protobuf and defined as [this protobuf structure](./meteoblue_dataset_sdk/Dataset.proto).

A 10 year hourly data series for 1 location requires `350 kb` using protobuf, compared to `1600 kb` using JSON. Additionally the meteoblue Python SDK transfers data using gzip which reduces the size to only `87 kb`. 

More detailed output of the `result` protobuf object:

```
geometries {
  domain: "NEMSGLOBAL"
  lats: 47.66651916503906
  lons: 7.5
  asls: 499.7736511230469
  locationNames: "Basel"
  nx: 1
  ny: 1
  timeResolution: "hourly"
  timeIntervals {
    start: 1546300800
    end: 1546387200
    stride: 3600
  }
  codes {
    code: 11
    level: "2 m above gnd"
    unit: "\302\260C"
    aggregation: "none"
    timeIntervals {
      data: 2.890000104904175
      data: 2.690000057220459
      data: 2.549999952316284
      data: 2.380000114440918
      data: 2.2699999809265137
      data: 2.119999885559082
      data: 1.9900000095367432
      data: 1.8300000429153442
      data: 1.8200000524520874
      data: 2.0999999046325684
      data: 2.430000066757202
      data: 2.9200000762939453
      data: 3.7200000286102295
      data: 3.930000066757202
      data: 3.9100000858306885
      data: 3.5299999713897705
      data: 3.130000114440918
      data: 2.880000114440918
      data: 2.6500000953674316
      data: 2.4600000381469727
      data: 2.2799999713897705
      data: 2.0299999713897705
      data: 1.690000057220459
      data: 1.3799999952316284
    }
  }
}
```
