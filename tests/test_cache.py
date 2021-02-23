from meteoblue_dataset_sdk.caching import FileCache

import os
import shutil
import tempfile
import zlib

from freezegun import freeze_time
from later.unittest import mock

# until we upgrade to >=3.8
from later.unittest.backport.async_case import IsolatedAsyncioTestCase


class TestFileCache(IsolatedAsyncioTestCase):
    def setUp(self):
        self.params = {
            "units": {
                "temperature": "C",
                "velocity": "km/h",
                "length": "metric",
                "energy": "watts",
            },
            "geometry": {
                "type": "MultiPoint",
                "coordinates": [[7.57327, 47.558399, 279]],
                "locationNames": ["Basel"],
            },
            "format": "json",
            "timeIntervals": ["2019-01-01T+00:00/2019-01-01T+00:00"],
            "timeIntervalsAlignment": "none",
            "queries": [
                {
                    "domain": "NEMSGLOBAL",
                    "gapFillDomain": None,
                    "timeResolution": "hourly",
                    "codes": [{"code": 11, "level": "2 m above gnd"}],
                }
            ],
        }

        self.cache_path = os.path.join(tempfile.gettempdir(), "mb_cache")
        if not os.path.exists(self.cache_path):
            os.mkdir(self.cache_path)
        self.dir_hash = "f4e"
        self.file_hash = "bb32678055481aa33398a8a7afaa5"
        self.dir_path = os.path.join(tempfile.gettempdir(), "mb_cache", self.dir_hash)
        self.file_path = os.path.join(
            tempfile.gettempdir(), "mb_cache", self.dir_hash, self.file_hash
        )

    def test__params_to_path_names(self):
        self.assertIsNone(FileCache._params_to_path_names({}))
        self.assertEqual(
            FileCache._params_to_path_names({"key": "value"}),
            ("88b", "ac95f31528d13a072c05f2a1cf371"),
        )

    def test_path(self):
        file_cache = FileCache()
        self.assertEqual(
            file_cache.cache_path, os.path.join(tempfile.gettempdir(), "mb_cache")
        )
        file_cache = FileCache(cache_path="/tmp/test_cache")
        self.assertEqual(file_cache.cache_path, "/tmp/test_cache/mb_cache")

    @freeze_time("2020-01-01 11:59:00", as_kwarg="valid_ts")
    @freeze_time("2020-01-01 06:00:00", as_kwarg="expired_ts")
    @freeze_time("2020-01-01 12:00:00", as_kwarg="mock_now")
    @mock.patch("os.path.getmtime")
    def test__is_cached_file_valid(self, mock_getmtime, **kwargs):
        mock_getmtime.return_value = kwargs.get("valid_ts").time_to_freeze.timestamp()
        file_cache = FileCache()
        self.assertTrue(file_cache._is_cached_file_valid("somepath"))
        mock_getmtime.return_value = kwargs.get("expired_ts").time_to_freeze.timestamp()
        file_cache = FileCache()
        self.assertFalse(file_cache._is_cached_file_valid("somepath"))

    @mock.patch("meteoblue_dataset_sdk.caching.FileCache._is_cached_file_valid")
    async def test_get(self, mock__is_cached_file_valid):

        os.mkdir(self.dir_path)
        with open(self.file_path, "wb") as file:
            file.write(zlib.compress(bytes('{"response": "data"}', "utf-8")))

        mock__is_cached_file_valid.return_value = True
        file_cache = FileCache()
        self.assertEqual(await file_cache.get(self.params), b'{"response": "data"}')
        mock__is_cached_file_valid.assert_called_with(
            f"{tempfile.gettempdir()}/mb_cache/{self.dir_hash}/{self.file_hash}"
        )

    @mock.patch("meteoblue_dataset_sdk.caching.FileCache._is_cached_file_valid")
    async def test_set(self, mock__is_cached_file_valid):
        mock__is_cached_file_valid.return_value = False
        file_cache = FileCache()
        await file_cache.set(self.params, bytes('{"someData": "superData"}', "utf-8"))
        with open(self.file_path, "rb") as file:
            self.assertEqual(zlib.decompress(file.read()), b'{"someData": "superData"}')

    def tearDown(self):
        if os.path.exists(self.cache_path):
            shutil.rmtree(self.cache_path, ignore_errors=True)
        super(TestFileCache, self).tearDown()
