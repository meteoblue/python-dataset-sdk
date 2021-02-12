""""
meteoblue dataset client
"""

import asyncio
import logging
from contextlib import asynccontextmanager

import aiohttp

from .caching import DEFAULT_CACHE_DURATION, Cache
from .Dataset_pb2 import DatasetApiProtobuf
from .utils import run_async


class ClientConfig(object):
    def __init__(self, apikey: str):
        # urls
        # following job id
        self.statusUrl = "http://my.meteoblue.com/queue/status/{}"
        # following api key
        self.queryUrl = "http://my.meteoblue.com/dataset/query?apikey={}"
        # following job id
        self.resultUrl = "http://queueresults.meteoblue.com/{}"

        # http
        self.httpMaxRetryCount = 5
        self.httpRetrySleepDuration = 1

        # other config
        self.apikey = apikey
        self.queueRetrySleepDuration = 5
        self.cleaning_interval = DEFAULT_CACHE_DURATION * 2


class Error(Exception):
    """Base class for exceptions in this module."""

    pass


class ApiError(Error):
    """Exception raised for errors by the dataset API

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message


class Client(object):
    def __init__(self, apikey: str):
        self._config = ClientConfig(apikey)
        self.cache = Cache()

    @asynccontextmanager
    async def _fetch(
        self,
        session: aiohttp.ClientSession,
        method: str,
        url: str,
        json: any = None,
    ):
        """
        Fetch data from an URL and try for error 5xx or timeouts.
        Codes other than 2xx will throw an exception.

        :param url: url to make http get on
        :param retryCount: number of retries to attempt
        :return:
        """
        logging.debug(f"Getting url {method} {url}")

        for retry in range(self._config.httpMaxRetryCount):
            async with session.request(method, url, json=json) as response:
                # return if successful
                if 200 <= response.status <= 299:
                    yield response

                # meteoblue APIs return a JSON encoded error message
                if response.status == 400 or response.status == 500:
                    json = await response.json()
                    logging.debug(
                        f"API returned error message: {json['error_message']}"
                    )
                    raise ApiError(json["error_message"])

                if retry == self._config.httpMaxRetryCount - 1:
                    logging.error(f"API returned unexpected error: {response.content}")
                    raise Exception("API returned unexpected error", response.content)

                # retry mechanism
                # check if request timed out or backend threw an error
                # if response.status == 408 or 500 <= response.status <= 599:
                logging.info(f"Request failed or timed out. Try {retry}")
                logging.debug(response)

    @asynccontextmanager
    async def _runOnJobQueue(self, session: aiohttp.ClientSession, params: dict):
        """
        Run the query on a job queue
        :param session: ClientSession
        :param params: query parameters for meteoblue dataset api
        :return: ClientResponse object from aiohttp lib
        """

        # Start job on a job queue
        logging.info("Starting job on queue")
        params["runOnJobQueue"] = True
        url = self._config.queryUrl.format(self._config.apikey)
        async with self._fetch(session, "POST", url, json=params) as response:
            responseJson = await response.json()

        # Wait until the job is finished
        jobId = responseJson["id"]
        logging.info(f"Waiting until job has finished (job id {jobId})")
        statusUrl = self._config.statusUrl.format(jobId)
        while True:
            async with self._fetch(session, "GET", statusUrl) as response:
                json = await response.json()
            status = json["status"]
            logging.debug(f"Job status is {status}")
            if status == "finished":
                break
            if status == "deleted":
                raise ApiError("Job was canceled")
            if status == "error":
                raise ApiError(json["error_message"])
            logging.info(
                f"Waiting 5 seconds for job to complete. Status: {status}, \
                job id {jobId}"
            )
            await asyncio.sleep(self._config.queueRetrySleepDuration)

        # Fetch the job queue result
        resultUrl = self._config.resultUrl.format(jobId)
        logging.debug(f"Fetching result for job id {jobId}")
        async with self._fetch(session, "GET", resultUrl) as response:
            yield response

    @asynccontextmanager
    async def queryRaw(self, params: dict):
        """
        Query meteoblue dataset api asynchronously and return a ClientResponse object
        using context manager
        :param params: query parameters
            see https://docs.meteoblue.com/en/apis/environmental-data/dataset-api
        :return: ClientResponse object from aiohttp lib
        """

        async with aiohttp.ClientSession() as session:
            # Try to run the job directly
            # In case the API throws an error, try to run it on a job queue
            try:
                url = self._config.queryUrl.format(self._config.apikey)
                async with self._fetch(session, "POST", url, json=params) as response:
                    yield response
            except ApiError as error:
                # Run on a job queue in case the api throws the error
                if error.message != "This job must be executed on a job-queue":
                    raise
                async with self._runOnJobQueue(session, params) as response:
                    yield response

    async def query(self, params: dict):
        """
        Query meteoblue dataset api asynchronously, transfer data using protobuf and
        return a structured object

        :param params:
            query parameters,
            see https://docs.meteoblue.com/en/apis/environmental-data/dataset-api
        :return: DatasetApiProtobuf object
        """

        params["format"] = "protobuf"
        cached_query_results = self.cache.get_query_results(params)
        if cached_query_results:
            return cached_query_results
        async with self.queryRaw(params) as response:
            data = await response.read()
            msg = DatasetApiProtobuf()
            msg.ParseFromString(data)
            # todo move to a couroutine
            self.cache.store_query_results(params, msg)
            return msg

    def querySync(self, params: dict):
        """
        Query meteoblue dataset api synchronously for sequential usage
        :param params:
             query parameters.
             see https://docs.meteoblue.com/en/apis/environmental-data/dataset-api
        :return: DatasetApiProtobuf object
        """
        return run_async(self.query, params)
