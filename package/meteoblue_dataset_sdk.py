""""
meteoblue dataset client
"""

import requests  # later use
import os
import hashlib
import time
import aiohttp
import asyncio

class MeteoblueDatasetClient(object):

    def __init__(self, apikey: str):
        self.apiKey = apikey

    # async def _check_status(self, queue_id: int):
    #     async with session.get('http://my.meteoblue.com/queue/status/' + queue_id) as response:
    #         if response.json()["status"] == "finished":
    #             break

    "Query async api dataset interface"
    async def query(self, params: dict):
        """
        query async dataset api interface
        :param params: params for meteoblue dataset api
        :return: result data set
        """

        directory = './apitemp/'
        tempfile = directory + hashlib.sha256(repr(params).encode('utf-8')).hexdigest()

        if not os.path.exists(directory):
            os.makedirs(directory)

        if os.path.isfile(tempfile):
            return tempfile

        r = requests.post('http://my.meteoblue.com/dataset/query?apikey=' + self.apiKey, json=params)
        # print(r.status_code)
        # print(r.content)

        # that doesn't work
        # if r.status_code == 200:
        #     with open(tempfile, 'wb+') as f:
        #         f.write(r.content)
        #     return tempfile

        if r.status_code != 400:
            raise Exception("API returned error", r.content)

        # job must be executed on a job queue
        error = r.json()
        if error['error_message'] != "This job must be executed on a job-queue":
            raise Exception("API returned error", error['error_message'])
        params["runOnJobQueue"] = True
        r = requests.post('http://my.meteoblue.com/dataset/query?apikey=' + self.apiKey, json=params)
        if r.status_code != 200:
            raise Exception("API returned error", r.content)
        queue = r.json()

        print("Job is queued")

        while True:
            #r = requests.get('http://my.meteoblue.com/queue/status/' + queue["id"])
            async with aiohttp.ClientSession() as session:
                async with session.get('http://my.meteoblue.com/queue/status/' + queue["id"]) as response:
                    if response.json()["status"] == "finished":
                        break
            print("Job status " + queue['status'] + ". Sleeping for 5 seconds")
            time.sleep(5)

        # file is now ready to download
        r = requests.get('http://queueresults.meteoblue.com/' + queue["id"])
        if r.status_code != 200:
            raise Exception("API returned error", r.content)

        with open(tempfile, 'wb+') as f:
            f.write(r.content)

        return tempfile
