import datetime
import hashlib
import os

CACHE_DIR = "mb_cache"
CACHE_PATH = os.path.join("/tmp", CACHE_DIR)
DEFAULT_CACHE_DURATION = 30


def write_query_to_cache(url: str):
    if not os.path.exists(CACHE_PATH):
        os.mkdir(CACHE_PATH)

    query_hash = _get_query_hash(url)
    query_dir_path = os.path.join(CACHE_PATH, query_hash)
    if os.path.exists(query_dir_path) and _get_valid_keys_in_dir(query_dir_path):
        return
    os.mkdir(query_dir_path)
    _store_query(query_dir_path)


def read_query_from_cache(url: str):
    query_hash = _get_query_hash(url)
    query_dir = os.path.join(CACHE_PATH, query_hash)
    if not os.path.exists(query_dir):
        return
    valid_keys = _get_valid_keys_in_dir(query_dir)
    if not valid_keys:
        return
    with open(os.path.join(query_dir, valid_keys[0]), "r") as file:
        print(file.readlines())
        return file.readlines()


def delete_expired_cache_keys():
    for query_dir in os.listdir(CACHE_PATH):
        all_keys_in_dir = _get_all_keys_in_dir(query_dir)
        for key, is_valid in all_keys_in_dir.items():
            if not is_valid:
                os.remove(os.path.join(CACHE_PATH, query_dir, key))


def _get_all_keys_in_dir(query_dir: str):
    dir_path = os.path.join(CACHE_PATH, query_dir)
    return {key: _is_cached_key_valid(key) for key in os.listdir(dir_path)}


def _get_valid_keys_in_dir(query_dir: str):
    all_keys = _get_all_keys_in_dir(query_dir)
    return [key for key, is_valid in all_keys.items() if is_valid]


def _is_cached_key_valid(key: str):
    key_as_datetime = datetime.datetime.fromtimestamp(int(key))
    cache_duration = datetime.datetime.now() - key_as_datetime
    return cache_duration.seconds < DEFAULT_CACHE_DURATION


def _store_query(query_dir_path: str):
    key_file_ts = str(round(datetime.datetime.now().timestamp()))
    with open(os.path.join(query_dir_path, key_file_ts), "x") as file:
        file.write("blabla")


def _get_query_hash(url: str):
    url_encoded = url.encode()
    hashed_url = hashlib.md5(url_encoded)
    return hashed_url.hexdigest()
