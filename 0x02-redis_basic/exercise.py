#!/usr/bin/env python3
"""Redis basic usage module"""
import redis
import uuid
from typing import Union, Callable, Optional


class Cache():
    """a class for using redis as a simple cache"""
    def __init__(self) -> None:
        """Init instance"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store data in db and return the key"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self,
            key: str,
            fn: Optional[Callable[[bytes], Union[bytes, str, int]]] = None
            ) -> Union[bytes, str, int, None]:
        """Retrieve and optionally convert the value of a given key
           from the cache
        """
        value = self._redis.get(key)
        if value and fn:
            value = fn(value)
        return value
