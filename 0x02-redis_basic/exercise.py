#!/usr/bin/env python3
"""Redis basic usage module"""
import redis
import uuid
from typing import Union


class Cache():
    """a class for using redis as a simple cache"""
    def __init__(self) -> None:
        """Init instance"""
        self._redis = redis.Redis()
        self._redis.flushdb

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store data in db and return the key"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
