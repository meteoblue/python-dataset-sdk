""""
meteoblue dataset client
"""

import os
import hashlib
import aiohttp
import asyncio
import logging


class ClientConfig(object):

    def __init__(self, apikey: str):
        self.url = {
            'status': 'http://my.meteoblue.com/queue/status/%s',  # following queue id
            'query': 'http://my.meteoblue.com/dataset/query?apikey=%s',  # following api key
            'result': 'http://queueresults.meteoblue.com/%s'  # following query id
        }
        self.tmp_directory = './api_temp/'
        self.apiKey = apikey
        self.tmp_file = None
        self.http_max_retry_count = 5


class Client(object):

    def __init__(self, apikey: str):
        logging.basicConfig(filename='mbdataset.log', level=logging.INFO)
        self._config = ClientConfig(apikey)

        if not os.path.exists(self._config.tmp_directory):
            os.makedirs(self._config.tmp_directory)

    async def __http_get(self, url: str, retry_count=0):
        logging.debug('Getting url %s' % url)
        logging.debug('Retry count: %s' % retry_count)

        async with self._session.get(url) as response:
            json = await response.json()

            # return if successful
            if 200 <= response.status <= 299:
                return json

            # retry mechanism
            if retry_count < self._config.http_max_retry_count:

                # check if request timed out or backend threw an error
                if response.status == 408 or 500 <= response.status <= 599:
                    # 408: HTTP request timeout
                    # 500-599: HTTP backend error
                    await asyncio.sleep(1)
                    return self.__http_get(url, retry_count + 1)

            logging.error('API returned error: %s' % response.content)
            raise Exception("API returned error", response.content)

    async def _job_finished(self, queue_id: int):
        """
        Wait until job has been processed by backend servers
        :param queue_id: id of queued job
        :return: json body with status information
        """
        url = self._config.url['status'] % str(queue_id)
        while True:
            json = await self.__http_get(url)
            logging.debug('Job status is %s' % json['status'])
            if json['status'] == 'finished':
                break
            logging.info('Waiting 5 more seconds for job to complete.')
            await asyncio.sleep(5)

    async def _submit_query(self, params: dict, retry_count=0):
        """
        Try to submit query to api
        :param params: query parameters for meteoblue dataset api
        :return: json body with status information
        """
        url = self._config.url['query'] % self._config.apiKey
        logging.debug('Posting data to url %s' % url)
        logging.debug('Retry count: %s' % retry_count)
        async with self._session.post(url, json=params) as response:
            json = await response.json()

            if 200 <= response.status <= 299:
                return json

            # retry mechanism
            if retry_count < self._config.http_max_retry_count:

                # check if request timed out or backend threw an error
                if response.status == 408 or 500 <= response.status <= 599:
                    # 408: HTTP request timeout
                    # 500-599: HTTP backend error
                    await asyncio.sleep(1)
                    return self._submit_query(params, retry_count + 1)

                # check if request needs to be executed on job queue
                if 400 <= response.status <= 499:
                    if 'error_message' in json:
                        if json['error_message'] == 'This job must be executed on a job-queue':
                            logging.info("Queueing job")
                            params["runOnJobQueue"] = True
                            return self._submit_query(params)

            logging.error('API returned error: %s' % response.content)
            raise Exception("API returned error", response.content)

    async def _fetch_result(self, queue_id):
        """
        Fetch api results and write to temp file
        :param queue_id: id of queued job
        :return: nothing/void
        """
        # self.__http_get() could be used here, too if we solve caching differently
        url = self._config.url['result'] % queue_id
        logging.debug('Fetching result(s) from url %s' % url)
        async with self._session.get(url) as response:
            with open(self._config.tmp_file, 'wb+') as f:
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
            queue = await self._submit_query(params)
            logging.info("Waiting until job has finished")
            await self._job_finished(queue['id'])
            await self._fetch_result(queue['id'])

    def query(self, params: dict):
        """
        Query async dataset api interface
        :param params: query parameters for meteoblue dataset api
        :return: file path containing results
        """

        self._config.tmp_file = self._config.tmp_directory + hashlib.sha256(repr(params).encode('utf-8')).hexdigest()
        if os.path.isfile(self._config.tmp_file):
            return self._config.tmp_file

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self._query(params))
        loop.close()

        return self._config.tmp_file
