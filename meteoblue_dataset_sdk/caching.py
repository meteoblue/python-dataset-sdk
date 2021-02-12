import datetime
import hashlib
import json
import os

CACHE_PATH = "/tmp/mb_cache"
DEFAULT_CACHE_DURATION = 30


class Cache:
    def __init__(self, cache_path=CACHE_PATH, cache_ttl=DEFAULT_CACHE_DURATION):
        if not os.path.exists(cache_path):
            os.mkdir(cache_path)

        self.cache_path = cache_path
        self.cache_ttl = cache_ttl
        self.cache_map = self._build_cache_map()

    def store_query_results(self, params: dict, data):
        query_hash = self._get_query_hash(params)
        if self._get_valid_keys_from_cache_map(query_hash):
            return
        self._write_query_to_cache(query_hash, data)

    def get_cached_query_results(self, params: dict):
        query_hash = self._get_query_hash(params)
        query_dir = os.path.join(self.cache_path, query_hash)
        valid_keys = self._get_valid_keys_from_cache_map(query_hash)
        if not valid_keys:
            return
        try:
            most_recent_key = valid_keys[0]
            with open(os.path.join(query_dir, most_recent_key), "r") as file:
                print(file.readlines())
                return file.readlines()
        except FileNotFoundError:
            print(query_dir, valid_keys[0], "not found")
            return

    def delete_expired_cache_keys(self):
        for query_hash, keys in self.cache_map.items():
            for key in list(keys):
                if not self._is_cached_key_valid(key):
                    os.remove(os.path.join(self.cache_path, query_hash, key))
                    keys.remove(key)

    def _get_valid_keys_from_cache_map(self, query_hash: str):
        all_keys_in_dir = self.cache_map.get(query_hash, [])
        return sorted(
            [key for key in all_keys_in_dir if self._is_cached_key_valid(key)],
            reverse=True,
        )

    def _is_cached_key_valid(self, key: str):
        key_as_datetime = datetime.datetime.fromtimestamp(int(key))
        cache_duration = datetime.datetime.now() - key_as_datetime
        return cache_duration.seconds < self.cache_ttl

    def _write_query_to_cache(self, query_hash: str, data):
        ts_as_key = str(round(datetime.datetime.now().timestamp()))
        query_dir_path = os.path.join(self.cache_path, query_hash)
        if not os.path.exists(query_dir_path):
            os.mkdir(query_dir_path)

        if self.cache_map.get(query_hash):
            self.cache_map[query_hash].append(ts_as_key)
        else:
            self.cache_map[query_hash] = [ts_as_key]

        with open(os.path.join(query_dir_path, ts_as_key), "x") as file:
            file.write(data)

    def _build_cache_map(self):
        cache_map = {}
        for query_dir_name, _, keys in os.walk(self.cache_path):
            cache_map[query_dir_name] = []
            for key in keys:
                if not self._is_cached_key_valid(key):
                    os.remove(os.path.join(self.cache_path, query_dir_name, key))
                cache_map[query_dir_name].append(key)
        return cache_map

    @staticmethod
    def _get_query_hash(query_params: dict):
        params_encoded = json.dumps(query_params).encode()
        hashed_params = hashlib.md5(params_encoded)
        return hashed_params.hexdigest()
