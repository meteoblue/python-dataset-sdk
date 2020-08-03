#!/usr/bin/env python3
"""
meteoblue dataset SDK to fetch data
"""

import requests
# import json
import os
import hashlib
import time


def meteoblue_dataset_query(query: dict, apikey: str):
    directory = './apitemp/'
    tempfile = directory+hashlib.sha256(repr(query).encode('utf-8')).hexdigest()

    if not os.path.exists(directory):
        os.makedirs(directory)

    if os.path.isfile(tempfile):
        return tempfile

    r = requests.post('http://my.meteoblue.com/dataset/query?apikey='+apikey, json=query)
    # print(r.status_code)
    # print(r.content)

    if r.status_code == 200:
        with open(tempfile, 'wb+') as f:
            f.write(r.content)
        return tempfile

    if r.status_code != 400:
        raise Exception("API returned error", r.content)

    # job must be executed on a job queue
    error = r.json()
    if error['error_message'] != "This job must be executed on a job-queue":
        raise Exception("API returned error", error['error_message'])
    query["runOnJobQueue"] = True
    r = requests.post('http://my.meteoblue.com/dataset/query?apikey='+apikey, json=query)
    if r.status_code != 200:
        raise Exception("API returned error", r.content)
    queue = r.json()

    print("Job is queued")

    while(True):
        r = requests.get('http://my.meteoblue.com/queue/status/'+queue["id"])
        queue = r.json()
        if queue["status"] == "finished":
            break

        print("Job status "+queue['status']+". Sleeping for 5 seconds")
        time.sleep(5)

    # file is now ready to download
    r = requests.get('http://queueresults.meteoblue.com/'+queue["id"])
    if r.status_code != 200:
        raise Exception("API returned error", r.content)

    with open(tempfile, 'wb+') as f:
        f.write(r.content)

    return tempfile


'''
def main():
    filename = meteoblue_dataset_query({
    "units": {
        "temperature": "C",
        "velocity": "km/h",
        "length": "metric",
        "energy": "watts"
    },
    "geometry": {
        "type": "Polygon",
        "coordinates": [
            [
                [
                    7.313768,
                    46.982946
                ],
                [
                    7.313768,
                    47.692346
                ],
                [
                    8.621369,
                    47.692346
                ],
                [
                    8.621369,
                    46.982946
                ],
                [
                    7.313768,
                    46.982946
                ]
            ]
        ]
    },
    "format": "netCDF",
    "timeIntervals": [
        "2000-01-01T+00:00/2019-01-04T+00:00"
    ],
    "timeIntervalsAlignment": "none",
    "queries": [
        {
            "domain": "NEMSGLOBAL",
            "gapFillDomain": None,
            "timeResolution": "hourly",
            "codes": [
                {
                    "code": 11,
                    "level": "2 m above gnd"
                }
            ]
        }
    ]
}, key)
    print(filename)


if __name__ == "__main__":
    main()
'''

