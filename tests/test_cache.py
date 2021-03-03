from meteoblue_dataset_sdk.caching import FileCache
from meteoblue_dataset_sdk.client import Client

import shutil
import tempfile
import zlib
from pathlib import Path

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

        self.cache_path = Path(tempfile.gettempdir(), "mb_cache")
        if not self.cache_path.exists():
            self.cache_path.mkdir()
        self.dir_hash = "f4e"
        self.file_hash = "bb32678055481aa33398a8a7afaa5"
        self.dir_path = Path(tempfile.gettempdir(), "mb_cache", self.dir_hash)
        self.file_path = Path(
            tempfile.gettempdir(), "mb_cache", self.dir_hash, self.file_hash
        )

    def test__hash_to_paths(self):
        self.assertEqual(FileCache._hash_to_paths(""), ("", ""))
        self.assertEqual(
            FileCache._hash_to_paths("88bac95f31528d13a072c05f2a1cf371"),
            ("88b", "ac95f31528d13a072c05f2a1cf371"),
        )

    def test_path(self):
        file_cache = FileCache()
        self.assertEqual(file_cache.cache_path, Path(tempfile.gettempdir(), "mb_cache"))
        file_cache = FileCache(path="/tmp/test_cache")
        self.assertEqual("/tmp/test_cache", file_cache.cache_path.as_posix())

    @mock.patch("pathlib.Path.exists", return_value=True)
    @mock.patch("aiofiles.os.stat")
    async def test__is_cached_file_valid(self, mock_stat, mock_path):
        file_cache = FileCache()
        with freeze_time("2020-01-01 12:00:00"):
            mock_stat.return_value.st_mtime = freeze_time(
                "2020-01-01 11:59:00"
            ).time_to_freeze.timestamp()
            self.assertTrue(await file_cache._is_cached_file_valid(Path("somepath")))

        with freeze_time("2020-01-01 12:00:00"):
            mock_stat.return_value.st_mtime = freeze_time(
                "2020-01-01 06:00:00"
            ).time_to_freeze.timestamp()
            self.assertFalse(await file_cache._is_cached_file_valid(Path("somepath")))

    @mock.patch("meteoblue_dataset_sdk.caching.FileCache._is_cached_file_valid")
    async def test_get(self, mock__is_cached_file_valid):

        self.dir_path.mkdir()
        with open(self.file_path, "wb") as file:
            file.write(zlib.compress(bytes('{"response": "data"}', "utf-8")))

        mock__is_cached_file_valid.return_value = True
        file_cache = FileCache()
        key = Client(apikey="124")._hash_params(self.params)
        self.assertEqual(await file_cache.get(key), b'{"response": "data"}')
        mock__is_cached_file_valid.assert_called_with(
            Path(tempfile.gettempdir(), "mb_cache", self.dir_hash, self.file_hash)
        )

    @mock.patch("meteoblue_dataset_sdk.caching.FileCache._is_cached_file_valid")
    async def test_set(self, mock__is_cached_file_valid):
        mock__is_cached_file_valid.return_value = False
        file_cache = FileCache()
        key = Client(apikey="124")._hash_params(self.params)
        await file_cache.set(key, bytes('{"someData": "superData"}', "utf-8"))
        with open(self.file_path, "rb") as file:
            self.assertEqual(zlib.decompress(file.read()), b'{"someData": "superData"}')

    def tearDown(self):
        if self.cache_path.exists():
            shutil.rmtree(self.cache_path, ignore_errors=True)
        super(TestFileCache, self).tearDown()
