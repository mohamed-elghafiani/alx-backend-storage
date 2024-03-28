#!/usr/bin/env python3
"""Redis basic usage module"""
import redis
import uuid
from typing import Union, Callable


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

    def get(self, key: str, fn: Callable[[bytes], str]) -> str:
        """Calls fun on the returned value of redis.get()"""
        value = self._redis.get(key)
        if fn:
            value = fn(value)
        return value
