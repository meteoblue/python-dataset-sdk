# Meteoblue Python Dataset SDK

## Prerequisites

### check default python version (e.g. on debian linux)
`python --version` should equal more than 3.6

otherwise switch version with
`update-alternatives --config python` as root

## Usage / Test

```
qparams = {'units': {'temperature': 'C', 'velocity': 'km/h', 'length': 'metric', 'energy': 'watts'}, 'geometry': {'type': 'Polygon', 'coordinates': [[[7.313768, 46.982946], [7.313768, 47.692346], [8.621369, 47.692346], [8.621369, 46.982946], [7.313768, 46.982946]]]}, 'format': 'netCDF', 'timeIntervals': ['2000-01-01T+00:00/2019-01-04T+00:00'], 'timeIntervalsAlignment': 'none', 'queries': [{'domain': 'NEMSGLOBAL', 'gapFillDomain': None, 'timeResolution': 'hourly', 'codes': [{'code': 11, 'level': '2 m above gnd'}]}]}
from meteoblue_dataset_sdk import *
mb = MeteoblueDatasetClient(apikey='XXXXXXXXXXXXXXX')  # ask for key
mb.query(qparams)
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
```
setuptools.setup(
    name="meteoblue-dataset-sdk", # Replace with your own username
    version="0.0.2",
    author="Jonas Wolff",
    author_email="jonas.wolff@meteoblue.com",
    description="Provides easy access to meteoblue dataset sdk.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/meteoblue/python-dataset-sdk",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
```

### Compile
`python setup.py bdist_wheel`

### Upload
`python -m twine upload --skip-existing dist/*`
