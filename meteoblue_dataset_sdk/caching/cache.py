import hashlib
import json
from abc import ABC, abstractmethod
from typing import ByteString


class Cache(ABC):
    @abstractmethod
    def set(self, query_params: dict, value: ByteString):
        pass

    @abstractmethod
    def get(self, query_params: dict):
        pass

    @staticmethod
    def _params_to_path_names(query_params: dict):
        if not query_params:
            return
        params_encoded = json.dumps(query_params).encode()
        hexdigest = hashlib.md5(params_encoded).hexdigest()
        dir_name = hexdigest[:4]
        file_name = hexdigest[4:]
        return dir_name, file_name
