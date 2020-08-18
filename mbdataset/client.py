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
        # urls
        self.status_url = 'http://my.meteoblue.com/queue/status/%s'  # following queue id
        self.query_url = 'http://my.meteoblue.com/dataset/query?apikey=%s'  # following api key
        self.result_url = 'http://queueresults.meteoblue.com/%s'  # following query id

        # http
        self.http_max_retry_count = 5

        # other config
        self.apikey = apikey
        self.log_file = 'mbdataset.log'


class Client(object):

    def __init__(self, apikey: str):
        self._config = ClientConfig(apikey)
        logging.basicConfig(
            filename=self._config.log_file,
            format='%(asctime)s %(levelname)-8s %(message)s',
            level=logging.DEBUG,
            datefmt='%Y-%m-%d %H:%M:%S')

        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)

    def __del__(self):
        self._loop.close()

    async def __http_get(self, session, url: str, retry_count=0):
        logging.debug('Getting url %s' % url)
        logging.debug('Retry count: %s' % retry_count)

        async with session.get(url) as response:
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
                    return self.__http_get(session, url, retry_count + 1)

            logging.error('API returned error: %s' % response.content)
            raise Exception("API returned error", response.content)

    async def _job_finished(self, session, queue_id: int):
        """
        Wait until job has been processed by backend servers
        :param queue_id: id of queued job
        :return: json body with status information
        """
        url = self._config.status_url % str(queue_id)
        while True:
            json = await self.__http_get(session, url)
            logging.debug('Job status is %s' % json['status'])
            if json['status'] == 'finished':
                break
            logging.info('Waiting 5 more seconds for job to complete.')
            await asyncio.sleep(5)

    async def _submit_query(self, session, params: dict, retry_count=0):
        """
        Try to submit query to api
        :param params: query parameters for meteoblue dataset api
        :return: json body with status information
        """
        url = self._config.query_url % self._config.apikey
        logging.debug('Posting data to url %s' % url)
        logging.debug('Retry count: %s' % retry_count)
        async with session.post(url, json=params) as response:
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
                    return self._submit_query(session, params, retry_count + 1)

                # check if request needs to be executed on job queue
                if 400 <= response.status <= 499:
                    if 'error_message' in json:
                        if json['error_message'] == 'This job must be executed on a job-queue':
                            logging.info("Queueing job")
                            params["runOnJobQueue"] = True
                            return await self._submit_query(session, params)

            logging.error('API returned error: %s' % response.content)
            raise Exception("API returned error", response.content)

    async def _fetch_result(self, session, queue_id):
        """
        Fetch api results and write to temp file
        :param queue_id: id of queued job
        :return: nothing/void
        """
        # self.__http_get() could be used here, too if we solve caching differently
        url = self._config.result_url % queue_id
        logging.debug('Fetching result(s) from url %s' % url)
        async with session.get(url) as response:
            return await response.json()

    async def _query(self, params: dict):
        """
        Call async functions
        :param params: query parameters for meteoblue dataset api
        :return: nothing/void
        """
        async with aiohttp.ClientSession() as session:
            queue = await self._submit_query(session, params)
            logging.info("Waiting until job has finished")
            await self._job_finished(session, queue['id'])
            return await self._fetch_result(session, queue['id'])

    async def query(self, params: dict):
        """
        Query async dataset api interface
        :param params: query parameters for meteoblue dataset api
        :return: json result data
        """

        await self._query(params)
        return await self._query(params)
        #return self._loop.run_until_complete(self._query(params))
