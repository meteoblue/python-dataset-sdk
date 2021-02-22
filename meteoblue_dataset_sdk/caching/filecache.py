import datetime
import logging
import os
import tempfile

import aiofiles
from aiofiles import os as aios
import zlib
from .cache import Cache

CACHE_DIR = "mb_cache"
# 7200s == 2h
DEFAULT_CACHE_DURATION = 7200


class FileCache(Cache):
    def __init__(self, cache_path=None, cache_ttl=DEFAULT_CACHE_DURATION, compression_level=6):
        if cache_path is None:
            cache_path = tempfile.gettempdir()
        cache_path = os.path.join(cache_path, CACHE_DIR)
        if not os.path.exists(cache_path):
            os.makedirs(cache_path)

        self.cache_path = cache_path
        self.cache_ttl = cache_ttl
        self.compression_level = compression_level

    async def set(self, query_params, value):
        if not query_params:
            return
        dir_name, file_name = self._params_to_path_names(query_params)
        dir_path = os.path.join(self.cache_path, dir_name)
        file_path = os.path.join(dir_path, file_name)
        if not os.path.exists(dir_path):
            await aios.mkdir(dir_path)
        if os.path.exists(file_path) and self._is_cached_file_valid(file_path):
            return
        temp_file_path = f"{file_path}~"
        async with aiofiles.open(temp_file_path, "wb") as file:
            await file.write(
                zlib.compress(value, self.compression_level)
            )
        await aios.rename(temp_file_path, file_path)

    async def get(self, query_params):
        if not query_params:
            return
        dir_name, file_name = self._params_to_path_names(query_params)
        file_path = os.path.join(self.cache_path, dir_name, file_name)
        if not os.path.exists(file_path) or not self._is_cached_file_valid(file_path):
            return
        try:
            async with aiofiles.open(file_path, "rb") as f:
                return zlib.decompress(await f.read())
        except (OSError, IOError) as e:
            logging.error(f"error while reading the file {file_path}", e)
            return

    def _is_cached_file_valid(self, file_path: str):
        file_modification_timestamp = int(os.path.getmtime(file_path))
        ts_as_datetime = datetime.datetime.fromtimestamp(file_modification_timestamp)
        cache_duration = datetime.datetime.now() - ts_as_datetime
        return cache_duration.seconds < self.cache_ttl
