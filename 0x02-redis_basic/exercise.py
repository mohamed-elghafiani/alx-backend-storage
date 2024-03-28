#!/usr/bin/env python3
"""Redis basic usage module"""
import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Return Wrapper for counting methods calls"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper function"""
        self._redis.incr(method.__qualname__, 1)

        return method(self, *args, **kwargs)

    return wrapper


class Cache():
    """a class for using redis as a simple cache"""
    def __init__(self) -> None:
        """Init instance"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
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

    def get_str(self, key: str) -> Optional[str]:
        """Retrieve a string value for a given key from the cache."""
        return self.get(key, fn=lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> Optional[int]:
        """Retrieve an int value for a given key from the cache."""
        return self.get(key, fn=int)
