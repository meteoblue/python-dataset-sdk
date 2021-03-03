from abc import ABC, abstractmethod


class AbstractCache(ABC):
    """
    Abstract class for the Cache implementation.
    Provide common methods to be implemented.
    """

    @abstractmethod
    async def set(self, key: str, value: bytes) -> None:
        """
        Store the value in the cache
        :param key: Key used to store the value
        :param value: The request data to store
        :return: None
        """
        raise NotImplementedError("Method must be implemented")

    @abstractmethod
    async def get(self, key: str) -> bytes:
        """
        Retrieve a value from the cache
        :param key: Key used to store the query to retrieve.
        :return: None if not found or the content of the file
        """
        raise NotImplementedError("Method must be implemented")
