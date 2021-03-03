""""
meteoblue dataset client
"""

import asyncio
import logging
from contextlib import asynccontextmanager
import hashlib
import json
import aiohttp

from .Dataset_pb2 import DatasetApiProtobuf
from .utils import run_async


class ClientConfig(object):
    def __init__(self, apikey: str):
        # urls
        # following job id
        self.status_url = "http://my.meteoblue.com/queue/status/{}"
        # following api key
        self.query_url = "http://my.meteoblue.com/dataset/query?apikey={}"
        # following job id
        self.result_url = "http://queueresults.meteoblue.com/{}"

        # http
        self.http_max_retry_count = 5
        self.http_retry_sleep_duration = 1

        # other config
        self.api_key = apikey
        self.queue_retry_sleep_duration = 5


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
    def __init__(self, apikey: str, cache=None):
        self._config = ClientConfig(apikey)
        self.cache = cache

    @asynccontextmanager
    async def _fetch(
        self,
        session: aiohttp.ClientSession,
        method: str,
        url: str,
        post_data: dict = None,
    ):
        """
        Fetch data from an URL and try for error 5xx or timeouts.
        Codes other than 2xx will throw an exception.
        :param url: url to call http GET on
        :param method: HTTP verb to use for the request
        :return: query_params: the parameters to use for the query
        """
        logging.debug(f"Getting url {method} {url}")
        for retry in range(self._config.http_max_retry_count):
            async with session.request(method, url, json=post_data) as response:
                # return if successful
                if 200 <= response.status <= 299:
                    yield response
                    return

                # meteoblue APIs return a JSON encoded error message
                if response.status == 400 or response.status == 500:
                    json_response = await response.json()
                    logging.debug(
                        f"API returned error message: {json_response['error_message']}"
                    )
                    raise ApiError(json_response["error_message"])

                if retry == self._config.http_max_retry_count - 1:
                    logging.error(f"API returned unexpected error: {response.content}")
                    raise Exception("API returned unexpected error", response.content)

                # retry mechanism
                # check if request timed out or backend threw an error
                # if response.status == 408 or 500 <= response.status <= 599:
                logging.info(f"Request failed or timed out. Try {retry}")
                logging.debug(response)

    @asynccontextmanager
    async def _run_on_job_queue(self, session: aiohttp.ClientSession, params: dict):
        """
        Run the query on a job queue
        :param session: ClientSession
        :param params: query parameters for meteoblue dataset api
        :return: ClientResponse object from aiohttp lib
        """

        # Start job on a job queue
        logging.info("Starting job on queue")
        params["runOnJobQueue"] = True
        url = self._config.query_url.format(self._config.api_key)
        async with self._fetch(session, "POST", url, post_data=params) as response:
            response_json = await response.json()

        # Wait until the job is finished
        job_id = response_json["id"]
        logging.info(f"Waiting until job has finished (job id {job_id})")
        status_url = self._config.status_url.format(job_id)
        while True:
            async with self._fetch(session, "GET", status_url) as response:
                json_data = await response.json()
            status = json_data["status"]
            logging.debug(f"Job status is {status}")
            if status == "finished":
                break
            if status == "deleted":
                raise ApiError("Job was canceled")
            if status == "error":
                raise ApiError(json_data["error_message"])
            logging.info(
                f"Waiting 5 seconds for job to complete. Status: {status}, \
                job id {job_id}"
            )
            await asyncio.sleep(self._config.queue_retry_sleep_duration)

        # Fetch the job queue result
        result_url = self._config.result_url.format(job_id)
        logging.debug(f"Fetching result for job id {job_id}")
        async with self._fetch(session, "GET", result_url) as response:
            yield response

    @asynccontextmanager
    async def _query_raw(self, params: dict):
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
                url = self._config.query_url.format(self._config.api_key)
                async with self._fetch(
                    session, "POST", url, post_data=params
                ) as response:
                    yield response
            except ApiError as error:
                # Run on a job queue in case the api throws the error
                if error.message != "This job must be executed on a job-queue":
                    raise
                async with self._run_on_job_queue(session, params) as response:
                    yield response

    @staticmethod
    def _hash_params(params: dict) -> str:
        return hashlib.md5(json.dumps(params).encode()).hexdigest()

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
        if self.cache:
            key = self._hash_params(params)
            cached_query_results = await self.cache.get(key)
            if cached_query_results:
                msg = DatasetApiProtobuf()
                msg.ParseFromString(cached_query_results)
                return msg

        async with self._query_raw(params) as response:
            data = await response.read()
            if self.cache:
                key = self._hash_params(params)
                await self.cache.set(key, data)
            msg = DatasetApiProtobuf()
            msg.ParseFromString(data)
            return msg

    def querySync(self, params: dict):
        """
        Query Meteoblue dataset api synchronously for sequential usage.
        Prefer query_sync in order to respect python semantic.
        :param params:
             query parameters.
             see https://docs.meteoblue.com/en/apis/environmental-data/dataset-api
        :return: DatasetApiProtobuf object
        """
        return run_async(self.query, params)

    def query_sync(self, params: dict):
        """
        Exactly the same as query sync but using underscore in the name.
        Keeping QuerySync for backward compatibility.
        """
        return self.querySync(params)
