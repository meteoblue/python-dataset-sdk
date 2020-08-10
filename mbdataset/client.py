""""
meteoblue dataset client
"""

# TODO: soft code urls
# TODO: check if temp fs is really necessary
# TODO: write exceptions for backend error(s)


import os
import hashlib
import aiohttp
import asyncio
import logging


class Client(object):

    def __init__(self, apikey: str):
        logging.basicConfig(filename='mbdataset.log', level=logging.INFO)

        self._apiKey = apikey
        self._tmp_directory = './api_temp/'
        self._tmp_file = None

        if not os.path.exists(self._tmp_directory):
            os.makedirs(self._tmp_directory)

    async def _job_finished(self, queue_id: int):
        """
        Wait until job has been processed by backend servers
        :param queue_id: id of queued job
        :return: json body with status information
        """
        while True:
            async with self._session.get('http://my.meteoblue.com/queue/status/' + str(queue_id)) as response:
                json = await response.json()
                if json["status"] == "finished":
                    break
            logging.info("Job status " + json['status'] + ". Sleeping for 5 seconds")
            await asyncio.sleep(5)

    async def _submit_query(self, params: dict):
        """
        Try to submit query to api
        :param params: query parameters for meteoblue dataset api
        :return: json body with status information
        """
        async with self._session.post(
                'http://my.meteoblue.com/dataset/query?apikey=' + self._apiKey, json=params) as response:
            json = await response.json()
            if 'runOnJobQueue' in params:
                if response.status != 200:
                    raise Exception("API returned error", response.content)
            else:
                if response.status != 400:
                    raise Exception("API returned error", response.content)
                if json['error_message'] != 'This job must be executed on a job-queue':
                    raise Exception("API returned error", json['error_message'])
            return json

    async def _fetch_result(self, queue_id):
        """
        Fetch api results and write to temp file
        :param queue_id: id of queued job
        :return: nothing/void
        """
        async with self._session.get('http://queueresults.meteoblue.com/' + queue_id) as response:
            with open(self._tmp_file, 'wb+') as f:
                while True:
                    chunk = await response.content.read(512)
                    if not chunk:
                        break
                    f.write(chunk)

    async def _query(self, params: dict):
        """
        Call async functions
        :param params: query parameters for meteoblue dataset api
        :return: nothing/void
        """
        async with aiohttp.ClientSession() as self._session:
            await self._submit_query(params)
            params["runOnJobQueue"] = True
            logging.info("Queueing job")
            queue_info = await self._submit_query(params)
            logging.info("Waiting until job has finished")
            await self._job_finished(queue_info['id'])
            await self._fetch_result(queue_info['id'])

    def query(self, params: dict):
        """
        Query async dataset api interface
        :param params: query parameters for meteoblue dataset api
        :return: file path containing results
        """

        self._tmp_file = self._tmp_directory + hashlib.sha256(repr(params).encode('utf-8')).hexdigest()
        if os.path.isfile(self._tmp_file):
            return self._tmp_file

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self._query(params))
        loop.close()

        return self._tmp_file
