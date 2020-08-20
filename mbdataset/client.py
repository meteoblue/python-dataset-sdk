""""
meteoblue dataset client
"""

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


class Client(object):

    def __init__(self, apikey: str):
        self._config = ClientConfig(apikey)

    async def __http_get(self, url: str, retry_count=0):
        """

        :param url: url to make http get on
        :param retry_count: number of retries to attempt
        :return:
        """
        logging.debug('Getting url %s' % url)
        logging.debug('Retry count: %s' % retry_count)

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                await response.json()

                # return if successful
                if 200 <= response.status <= 299:
                    return response

                # retry mechanism
                if retry_count < self._config.http_max_retry_count:

                    # check if request timed out or backend threw an error
                    if response.status == 408 or 500 <= response.status <= 599:
                        # 408: HTTP request timeout
                        # 500-599: HTTP backend error
                        await asyncio.sleep(1)
                        return await self.__http_get(url, retry_count + 1)

            logging.error('API returned error: %s' % response.content)
            raise Exception("API returned error", response.content)

    async def _job_finished(self, queue_id: int):
        """
        Wait until job has been processed by backend servers
        :param queue_id: id of queued job
        :return: json body with status information
        """
        url = self._config.status_url % str(queue_id)
        while True:
            http_response = await self.__http_get(url)
            json = await http_response.json()
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
        url = self._config.query_url % self._config.apikey
        logging.debug('Posting data to url %s' % url)
        logging.debug('Retry count: %s' % retry_count)

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=params) as response:
                json = await response.json()

                if 200 <= response.status <= 299:
                    return response

                # retry mechanism
                if retry_count < self._config.http_max_retry_count:

                    # check if request timed out or backend threw an error
                    if response.status == 408 or 500 <= response.status <= 599:
                        # 408: HTTP request timeout
                        # 500-599: HTTP backend error
                        await asyncio.sleep(1)
                        return await self._submit_query(params, retry_count + 1)

                    # check if request needs to be executed on job queue
                    if 400 <= response.status <= 499:
                        if 'error_message' in json:
                            if json['error_message'] == 'This job must be executed on a job-queue':
                                logging.info("Queueing job")
                                params["runOnJobQueue"] = True
                                return await self._submit_query(params)

            logging.error('API returned error: %s' % response.content)
            raise Exception("API returned error", response.content)

    async def _fetch_result(self, queue_id):
        """
        Fetch api results and write to temp file
        :param queue_id: id of queued job
        :return: nothing/void
        """
        # self.__http_get() could be used here, too if we solve caching differently
        url = self._config.result_url % queue_id
        logging.debug('Fetching result(s) from url %s' % url)
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return response

    async def _query(self, params: dict):
        """
        Call async functions
        :param params: query parameters for meteoblue dataset api
        :return: ClientResponse object from aiohttp lib
        """
        submit_response = await self._submit_query(params)
        submit_response_json = await submit_response.json()

        # if there is no id, request doesn't have to be queued
        # this must be the final result
        if 'id' not in submit_response_json:
            return submit_response

        # watch queue
        queue_id = submit_response_json['id']
        logging.info("%s: Waiting until job has finished" % queue_id)
        await self._job_finished(queue_id)

        return await self._fetch_result(queue_id)

    def query(self, params: dict):
        """
        Query meteoblue dataset api synchronously for sequential usage
        :param params: query parameters, see https://docs.meteoblue.com/en/apis/environmental-data/dataset-api
        :return: ClientResponse object from aiohttp lib
        """
        return self.query_seq(params)

    def query_seq(self, params: dict):
        """
        Query meteoblue dataset api synchronously for sequential usage
        :param params: query parameters, see https://docs.meteoblue.com/en/apis/environmental-data/dataset-api
        :return: ClientResponse object from aiohttp lib
        """
        return asyncio.run(self._query(params))

    async def query_parallel(self, params: dict):
        """
        Query meteoblue dataset api asynchronously, run multiple queries in parallel
        :param params: query parameters, see https://docs.meteoblue.com/en/apis/environmental-data/dataset-api
        :return: ClientResponse object from aiohttp lib
        """
        return await self._query(params)


async def main():
    qparams = {'units': {'temperature': 'C', 'velocity': 'km/h', 'length': 'metric', 'energy': 'watts'},
               'geometry': {'type': 'Polygon', 'coordinates': [
                   [[7.313768, 46.982946], [7.313768, 47.692346], [8.621369, 47.692346], [8.621369, 46.982946],
                    [7.313768, 46.982946]]]}, 'format': 'json',
               'timeIntervals': ['2000-01-01T+00:00/2019-01-04T+00:00'], 'timeIntervalsAlignment': 'none', 'queries': [
            {'domain': 'NEMSGLOBAL', 'gapFillDomain': None, 'timeResolution': 'hourly',
             'codes': [{'code': 11, 'level': '2 m above gnd'}]}]}
    # import mbdataset
    mb = Client(apikey='xxxxxxx')  # ask for key
    query1 = asyncio.create_task(mb.query(qparams))
    query2 = asyncio.create_task(mb.query(qparams))
    res1 = await query1
    res2 = await query2
    # print(res1)
    # print(res2)


if __name__ == "__main__":
    logging.basicConfig(
        # filename=self._config.log_file,
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.DEBUG,
        datefmt='%Y-%m-%d %H:%M:%S')

    asyncio.run(main())
