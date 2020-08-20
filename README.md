# Meteoblue Python Dataset SDK

## Prerequisites

### check default python version (e.g. on debian linux)
`python --version` should equal more than 3.6

otherwise switch version with
`update-alternatives --config python` as root

## Usage / Test

### Install module from pip
`pip3 install mbdataset`

### Query some data
```
qparams = {'units': {'temperature': 'C', 'velocity': 'km/h', 'length': 'metric', 'energy': 'watts'}, 'geometry': {'type': 'Polygon', 'coordinates': [[[7.313768, 46.982946], [7.313768, 47.692346], [8.621369, 47.692346], [8.621369, 46.982946], [7.313768, 46.982946]]]}, 'format': 'json', 'timeIntervals': ['2000-01-01T+00:00/2019-01-04T+00:00'], 'timeIntervalsAlignment': 'none', 'queries': [{'domain': 'NEMSGLOBAL', 'gapFillDomain': None, 'timeResolution': 'hourly', 'codes': [{'code': 11, 'level': '2 m above gnd'}]}]}  # use queue
qparams = {"units":{"temperature":"C","velocity":"km/h","length":"metric","energy":"watts"},"geometry":{"type":"MultiPoint","coordinates":[[7.57327,47.558399,279]],"locationNames":["Basel"]},"format":"json","timeIntervals":["2019-01-01T+00:00/2019-01-01T+00:00"],"timeIntervalsAlignment":"none","queries":[{"domain":"NEMSGLOBAL","gapFillDomain":null,"timeResolution":"hourly","codes":[{"code":157,"level":"180-0 mb above gnd"}]}]}  # not use queue
import mbdataset
mb = mbdataset.Client(apikey='XXXXXXXXXXXXXXX')  # ask for key
print(mb.query(qparams))
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
