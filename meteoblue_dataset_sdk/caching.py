# import datetime
# import hashlib
# import json
# import os
# import tempfile
#
# import aiofiles
# from aiofiles import os as aios
#
# CACHE_DIR = "mb_cache"
# # 7200s == 2h
# DEFAULT_CACHE_DURATION = 7200
#
#
# class Cache:
#     def __init__(self, cache_path=None, cache_ttl=DEFAULT_CACHE_DURATION):
#         if cache_path is None:
#             cache_path = tempfile.gettempdir()
#         cache_path = os.path.join(cache_path, CACHE_DIR)
#         if not os.path.exists(cache_path):
#             os.mkdir(cache_path)
#
#         self.cache_path = cache_path
#         self.cache_ttl = cache_ttl
#         self.cached_files = self._get_cached_files_list()
#
#     async def store_query_results(self, params: dict, data):
#         if not params:
#             return
#         query_hash = self._hash_params(params)
#         if self._get_valid_cached_queries(query_hash):
#             return
#         ts_as_key = round(datetime.datetime.now().timestamp())
#         query_cache_filename = f"{query_hash}_{ts_as_key}"
#         query_cache_file = os.path.join(self.cache_path, query_cache_filename)
#         async with aiofiles.open(query_cache_file, "x") as file:
#             await file.write(data)
#         self.cached_files.append(query_cache_filename)
#
#     async def get_query_results(self, params: dict):
#         if not params:
#             return
#         query_hash = self._hash_params(params)
#         valid_caches = self._get_valid_cached_queries(query_hash)
#         if not valid_caches:
#             return
#         try:
#             most_recent_key = valid_caches[0]
#             async with aiofiles.open(
#                 os.path.join(self.cache_path, most_recent_key), "r"
#             ) as f:
#                 return await f.read()
#         except FileNotFoundError:
#             print(valid_caches[0], "not found")
#             return
#
#     async def delete_expired_caches(self):
#         for query_filename in list(self.cached_files):
#             query_hash, timestamp = query_filename.split("_")
#             if self._is_cached_query_valid(timestamp):
#                 continue
#                 # todo: async?
#             await aios.remove(os.path.join(self.cache_path, query_hash, timestamp))
#             self.cached_files.remove(query_filename)
#
#     def _get_valid_cached_queries(self, query_hash: str):
#         valid_cached_queries = []
#         for cached_filename in self.cached_files:
#             cache_hash, timestamp = cached_filename.split("_")
#             if query_hash != cache_hash or not self._is_cached_query_valid(timestamp):
#                 continue
#             valid_cached_queries.append(cached_filename)
#         return sorted(valid_cached_queries, key=lambda x: x.split("_")[1], reverse=True)
#
#     def _is_cached_query_valid(self, timestamp: str):
#         key_as_datetime = datetime.datetime.fromtimestamp(int(timestamp))
#         cache_duration = datetime.datetime.now() - key_as_datetime
#         return cache_duration.seconds < self.cache_ttl
#
#     def _get_cached_files_list(self):
#         valid_cache_files = []
#         for query_filename in os.listdir(self.cache_path):
#             query_hash, timestamp = query_filename.split("_")
#             if not self._is_cached_query_valid(timestamp):
#                 continue
#             valid_cache_files.append(query_filename)
#         return valid_cache_files
#
#     @staticmethod
#     def _hash_params(query_params: dict):
#         params_encoded = json.dumps(query_params).encode()
#         hashed_params = hashlib.md5(params_encoded)
#         return hashed_params.hexdigest()


class Cache:

    def __init__(self, redis_config=None):
     self.redis_config = redis_config

     def set(self):
        if self.redis_config:
         self.set_with_redis()

    def set_with_redis(self):
       pass

    def set_with_filecache(self):
       pass



