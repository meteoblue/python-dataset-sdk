import datetime
import logging
import tempfile
import zlib
from typing import Optional
from pathlib import Path
import aiofiles
import aiofiles.os

from .abstractcache import AbstractCache

DEFAULT_CACHE_DIR = "mb_cache"
# 7200s == 2h
DEFAULT_CACHE_DURATION = 7200


class FileCache(AbstractCache):
    def __init__(
        self,
        path: Optional[str] = None,
        max_age: int = DEFAULT_CACHE_DURATION,
        compression_level: int = zlib.Z_DEFAULT_COMPRESSION,
    ):
        """
        Local file storage class
        :param path: Custom local cache storage path. Default to
        /SYSTEM_TEMP_FOLDER/mb_cache
        :param max_age: Cache retention period in seconds
        :param compression_level: Zlib compression level used to compressed the bytes
        input
        """
        cache_path = Path(tempfile.gettempdir(), DEFAULT_CACHE_DIR)
        if path is not None:
            cache_path = Path(path)
        if not cache_path.exists():
            cache_path.mkdir(parents=True)

        self.cache_path = cache_path
        self.max_age = max_age
        self.compression_level = compression_level

    async def set(self, key: str, value: bytes) -> None:
        """ "
        Hash the query params and use its value a directory and file name.
        If there is already a valid cache file existing, it will exit. Otherwise it
        will write to a temporary file before renaming it.
        :param key: Key used to store the value
        :param value: The request data to store
        """
        if not key:
            return
        dir_name, file_name = self._hash_to_paths(key)
        cache_file_path = Path(self.cache_path, dir_name, file_name)
        # dir_path, file_path = cache_file_path.parent, cache_file_path.name

        try:
            await aiofiles.os.stat(cache_file_path.parent)
        except FileNotFoundError:
            await aiofiles.os.mkdir(cache_file_path.parent)

        if await self._is_cached_file_valid(cache_file_path):
            return
        temp_file_path = f"{cache_file_path}~"
        async with aiofiles.open(temp_file_path, "wb") as file:
            await file.write(zlib.compress(value, self.compression_level))
        await aiofiles.os.rename(temp_file_path, cache_file_path)

    async def get(self, key: str) -> Optional[bytes]:
        if not key:
            return
        dir_name, file_name = self._hash_to_paths(key)
        file_path = Path(self.cache_path, dir_name, file_name)
        if not await self._is_cached_file_valid(file_path):
            return
        try:
            async with aiofiles.open(file_path, "rb") as f:
                return zlib.decompress(await f.read())
        except (OSError, IOError) as e:
            logging.error(f"error while reading the file {file_path}", e)
            return

    async def _is_cached_file_valid(self, file_path: Path) -> bool:
        if not file_path.exists():
            return False
        stats = await aiofiles.os.stat(file_path)
        file_modification_timestamp = int(stats.st_mtime)
        ts_as_datetime = datetime.datetime.fromtimestamp(file_modification_timestamp)
        cache_duration = datetime.datetime.now() - ts_as_datetime
        return cache_duration.seconds < self.max_age

    @staticmethod
    def _hash_to_paths(key_hash: str) -> tuple:
        """
        Split the hash in two part: the directory and the file.
        :param key_hash: Request parameters to use a key.
        :return: The first 3 characters of the hash as the directory name and the rest
        as the filename.
        """
        return key_hash[:3], key_hash[3:]
