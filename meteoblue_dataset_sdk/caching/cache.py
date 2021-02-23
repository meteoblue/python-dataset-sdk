from abc import ABC, abstractmethod


class Cache(ABC):
    """
    Base class for the Cache implementation. Provide common methods to be implemented
    """

    @abstractmethod
    def set(self, query_params: dict, value: bytes):
        """
        Store the value in the cache
        :param query_params: query parameters of the query to be stored. Must be hashed
        and used as key
        :param value: The request data to store
        :return: None
        """
        pass

    @abstractmethod
    def get(self, query_params: dict) -> bytes:
        """
        Retrieve a value from the cache
        :param query_params: query parameters of the query to retrieve. It must be
        hashed with the same method used in self.set in order to be retrieved.
        :return: None if not found or the content of the file
        """
        pass
