import datetime
import os
import tempfile

import aiofiles
from aiofiles import os as aios

from .cache import Cache

CACHE_DIR = "mb_cache"
# 7200s == 2h
DEFAULT_CACHE_DURATION = 7200


class FileCache(Cache):
    def __init__(self, cache_path=None, cache_ttl=DEFAULT_CACHE_DURATION):
        if cache_path is None:
            cache_path = tempfile.gettempdir()
        cache_path = os.path.join(cache_path, CACHE_DIR)
        if not os.path.exists(cache_path):
            os.mkdir(cache_path)

        self.cache_path = cache_path
        self.cache_ttl = cache_ttl

    async def set(self, query_params, value):
        if not query_params:
            return
        hashed_params = self._params_to_hash(query_params)
        file_name = str(round(datetime.datetime.now().timestamp()))
        query_dir_path = os.path.join(self.cache_path, hashed_params)
        if not os.path.exists(query_dir_path):
            await aios.mkdir(query_dir_path)
        if self._get_latest_cached_file(query_dir_path):
            return
        temp_file_path = os.path.join(query_dir_path, f"{file_name}~")
        async with aiofiles.open(temp_file_path, "wb") as file:
            await file.write(value)
        await aios.rename(temp_file_path, temp_file_path.rstrip("~"))

    async def get(self, query_params):
        if not query_params:
            return
        query_hash = self._params_to_hash(query_params)
        query_dir_path = os.path.join(self.cache_path, query_hash)
        if not os.path.exists(query_dir_path):
            return
        most_recent_file = self._get_latest_cached_file(query_dir_path)
        if not most_recent_file:
            return
        try:
            most_recent_file_path = os.path.join(query_dir_path, most_recent_file)
            async with aiofiles.open(most_recent_file_path, "rb") as f:
                return await f.read()
        except FileNotFoundError:
            print(os.path.join(self.cache_path, most_recent_file), "not found")
            return

    def _is_cached_query_valid(self, timestamp: str):
        key_as_datetime = datetime.datetime.fromtimestamp(int(timestamp))
        cache_duration = datetime.datetime.now() - key_as_datetime
        return cache_duration.seconds < self.cache_ttl

    def _get_latest_cached_file(self, dir_path: str):
        cached_files = [
            file
            for file in os.listdir(dir_path)
            if not file.find("~") and self._is_cached_query_valid(file)
        ]
        if not cached_files:
            return
        return max(cached_files)
