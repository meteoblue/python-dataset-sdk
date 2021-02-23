import datetime
import hashlib
import json
import logging
import os
import tempfile
import zlib
from typing import Union, Optional

import aiofiles
from aiofiles import os as aios

from .cache import Cache

CACHE_DIR = "mb_cache"
# 7200s == 2h
DEFAULT_CACHE_DURATION = 7200


class FileCache(Cache):
    def __init__(
        self,
        cache_path: Optional[str] = None,
        cache_ttl: int = DEFAULT_CACHE_DURATION,
        compression_level: int = 6,
    ):
        if cache_path is None:
            cache_path = tempfile.gettempdir()
        cache_path = os.path.join(cache_path, CACHE_DIR)
        if not os.path.exists(cache_path):
            os.makedirs(cache_path)

        self.cache_path = cache_path
        self.cache_ttl = cache_ttl
        self.compression_level = compression_level

    async def set(self, query_params: dict, value: bytes) -> None:
        """ "
        Hash the query params and use its value a directory and file name.
        If there is already a valid cache file existing, it will exit. Otherwise it
        will write to a temporary file before renaming it.
        :param query_params: query parameters of the query to be stored.
        :param value: The request data to store
        """
        if not query_params:
            return
        dir_name, file_name = self._params_to_path_names(query_params)
        dir_path = os.path.join(self.cache_path, dir_name)
        file_path = os.path.join(dir_path, file_name)
        if not os.path.exists(dir_path):
            await aios.mkdir(dir_path)
        if self._is_cached_file_valid(file_path):
            return
        temp_file_path = f"{file_path}~"
        async with aiofiles.open(temp_file_path, "wb") as file:
            await file.write(zlib.compress(value, self.compression_level))
        await aios.rename(temp_file_path, file_path)

    async def get(self, query_params: dict) -> Union[None, bytes]:
        """
        Retrieve a value from a cached file based on the hash of query param.
        :param query_params: query parameters to be retrieved
        :return: None if no valid cache file or bytes
        """
        if not query_params:
            return
        dir_name, file_name = self._params_to_path_names(query_params)
        file_path = os.path.join(self.cache_path, dir_name, file_name)
        if not self._is_cached_file_valid(file_path):
            return
        try:
            async with aiofiles.open(file_path, "rb") as f:
                return zlib.decompress(await f.read())
        except (OSError, IOError) as e:
            logging.error(f"error while reading the file {file_path}", e)
            return

    def _is_cached_file_valid(self, file_path: str) -> bool:
        """
        Verify if the given file is not expired
        :param file_path: path of the cached file: mb_cache/1sd/23btyqs5rfzm
        :return: True/False if the file exists and is valid
        """
        if not os.path.exists(file_path):
            return False
        file_modification_timestamp = int(os.path.getmtime(file_path))
        ts_as_datetime = datetime.datetime.fromtimestamp(file_modification_timestamp)
        cache_duration = datetime.datetime.now() - ts_as_datetime
        return cache_duration.seconds < self.cache_ttl

    @staticmethod
    def _params_to_path_names(query_params: dict) -> Union[None, tuple]:
        """
        Hash the query_params and return the path file path.
        :param query_params: Request parameters to use a key.
        :return: The first 3 characters of the hash as the directory name and the rest
        as the filename. None if no query_params provided.
        """
        if not query_params:
            return
        params_encoded = json.dumps(query_params).encode()
        hexdigest = hashlib.md5(params_encoded).hexdigest()
        dir_name = hexdigest[:3]
        file_name = hexdigest[3:]
        return dir_name, file_name
