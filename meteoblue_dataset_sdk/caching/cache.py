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
    def _params_to_hash(query_params: dict):
        params_encoded = json.dumps(query_params).encode()
        return hashlib.md5(params_encoded).hexdigest()
