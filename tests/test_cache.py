import os
import unittest
from unittest import IsolatedAsyncioTestCase, mock

import aiofiles
from freezegun import freeze_time

from meteoblue_dataset_sdk.caching import Cache


class TestCache(unittest.TestCase):
    def test_hash_params(self):
        cache = Cache()
        self.assertEqual(
            "c06d4357174f0eb882003a868b93909a", cache._hash_params({"param1": 32})
        )

    @mock.patch("os.listdir")
    @mock.patch("os.mkdir")
    @mock.patch("tempfile.gettempdir")
    def test_cache_path(self, path_mock, mkdir_mock, mock_listdir):
        path_mock.return_value = "/somewhere"
        mock_listdir.return_value = []
        cache = Cache()
        self.assertEqual(cache.cache_path, "/somewhere/mb_cache")
        cache = Cache(cache_path="/tmp")
        self.assertEqual(cache.cache_path, "/tmp/mb_cache")

    @freeze_time("2020-01-01 06:00:00", as_kwarg="mock_expired_cache")
    @freeze_time("2020-01-01 11:58:00", as_kwarg="mock_valid_cache")
    @freeze_time("2020-01-01 12:00:00", as_kwarg="mock_now")
    @mock.patch("os.listdir")
    def test_get_cached_files_list(self, mock_listdir, **kwargs):
        mock_listdir.return_value = []
        cache = Cache()
        self.assertEqual([], cache._get_cached_files_list())

        expired_ts = int(kwargs.get("mock_expired_cache").time_to_freeze.timestamp())
        valid_ts = int(kwargs.get("mock_valid_cache").time_to_freeze.timestamp())
        mock_listdir.return_value = [f"somehash_{expired_ts}", f"somehash_{valid_ts}"]
        self.assertEqual([f"somehash_{valid_ts}"], cache._get_cached_files_list())


class TestAsyncCaching(IsolatedAsyncioTestCase):
    async def test_no_get_query_results(self):
        cache = Cache()
        no_param = await cache.get_query_results({})
        self.assertEqual(None, no_param)

        query_results_not_stored = await cache.get_query_results(
            {
                "units": {
                    "temperature": "C",
                    "velocity": "km/h",
                    "length": "metric",
                    "energy": "watts",
                }
            }
        )
        self.assertEqual(None, query_results_not_stored)

    async def test_get_query_results_integration(self):
        cache = Cache(cache_path="/tmp/")
        params = {
            "units": {
                "temperature": "C",
                "velocity": "km/h",
                "length": "metric",
                "energy": "watts",
            }
        }
        data = {"key": "value"}
        await cache.store_query_results(params, data=str(data))
        cached_results = await cache.get_query_results(params)
        self.assertEqual(cached_results, str(data))

    async def test_store_query_results_integration(self):
        cache = Cache(cache_path="/tmp/")
        params = {
            "units": {
                "temperature": "C",
                "velocity": "km/h",
                "length": "metric",
                "energy": "watts",
            }
        }
        data ={"key": "value"}

        await cache.store_query_results(params, data=str(data))
        self.assertEqual(len(cache.cached_files), 1)
        async with aiofiles.open(
            os.path.join("/tmp/mb_cache", cache.cached_files[0])
        ) as f:
            content = await f.read()
            self.assertEqual(content, str(data))


    async def asyncTearDown(self):
        await Cache().delete_expired_caches()

    # @freeze_time("2020-01-01 12:00:00", as_arg="mock_ts")
    # @mock.patch("meteoblue_dataset_sdk.caching.Cache._get_valid_cached_queries")
    # @mock.patch("aiofiles.open")
    # async def test_get_query_results(
    #     self, mock_aio_open, mock_get_valid_cached_queries, mock_ts
    # ):
    #     ts = int(mock_ts.get("mock_expired_cache").time_to_freeze.timestamp())
    #     params = {
    #         "units": {
    #             "temperature": "C",
    #             "velocity": "km/h",
    #             "length": "metric",
    #             "energy": "watts",
    #         }
    #     }
    #     data = {"key": "value"}
    #     filename = f"{Cache._hash_params(params)}_{ts}"
    #     mock_get_valid_cached_queries = [
    #         filename,
    #     ]
    #     cache = Cache(cache_path="/tmp/")
    #     mock_aio_open = mock.mock_open(read_data=str(data))
    #     print(await cache.get_query_results(params))
