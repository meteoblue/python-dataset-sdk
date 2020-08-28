# meteoblue Python Dataset SDK

This library simplifies access to the [meteoblue dataset API](https://docs.meteoblue.com/en/apis/environmental-data/dataset-api)

Features:
- Fetch any dataset from the meteoblue environmental data archive
- Transparently integrates job queues to query large datasets
- Efficiently transfers data using compressed protobuf messages
- Asynchronous interface to query data in parallel
- Data can be used as simple floating-point arrays. No further formatting required.


## Installation
- Ensure that you are using at least Python 3.7 with `python --version` 
- Install the module with `pip3 install mbdataset`

This module will also install the following dependencies automatically:
- aiohttp >=3.6,<4
- protobuf >=3.0,<4

## Usage
```python
import mbdataset

async def myFunction():
    # Query 1 year of hourly temperature for Basel from meteoblue NEMSGLOBAL
    query = {"geometry": {"type": "MultiPoint", "coordinates": [[7.57327, 47.558399, 279]], "locationNames": ["Basel"]}, "format": "json", "timeIntervals": [
            "2019-01-01T+00:00/2019-01-01T+00:00"], "queries": [{"domain": "NEMSGLOBAL", "timeResolution": "hourly", "codes": [{"code": 11, "level": "2 m above gnd"}]}]}

    client = mbdataset.Client(apikey='XXXXXXXXXXXXXXX')
    result = await client.query(query)
    # result is a structured object containing timestamps and data

    timestamps = result.geometries[0].timeIntervals[0].timestamps
    data = result.geometries[0].codes[0].timeIntervals[0].data

    print(timestamps)
    # [1546300800, 1546304400, 1546308000, 1546311600, 1546315200, ...
    print(data)
    # [2.89, 2.69, 2.549999, 2.3800001,
```

More detailed output:

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
    timestamps: 1546300800
    timestamps: 1546304400
    timestamps: 1546308000
    timestamps: 1546311600
    timestamps: 1546315200
    timestamps: 1546318800
    timestamps: 1546322400
    timestamps: 1546326000
    timestamps: 1546329600
    timestamps: 1546333200
    timestamps: 1546336800
    timestamps: 1546340400
    timestamps: 1546344000
    timestamps: 1546347600
    timestamps: 1546351200
    timestamps: 1546354800
    timestamps: 1546358400
    timestamps: 1546362000
    timestamps: 1546365600
    timestamps: 1546369200
    timestamps: 1546372800
    timestamps: 1546376400
    timestamps: 1546380000
    timestamps: 1546383600
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


## Developer setup
```bash
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
```

## Build pip package

### One time config
```python -V  # for python version (2/3)
python -m pip --version
python -m pip install --upgrade pip setuptools wheel
python -m pip install tqdm
python -m pip install --user --upgrade twine
```
```
cat <<EOF > ~/.pypirc
[distutils] 
index-servers=pypi
[pypi] 
repository = https://upload.pypi.org/legacy/ 
username = meteoblue
EOF
```

### Update metadata in setup.py
See [setup.py](setup.py).

### Compile
`python3 setup.py sdist bdist_wheel`

### Upload
`python3 -m twine upload --skip-existing dist/* --non-interactive -p XXXXXXXXXXXXXXXXXXXX`
