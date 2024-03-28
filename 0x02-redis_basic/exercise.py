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


def call_history(method: Callable) -> Callable:
    """Return Wrapper for counting methods calls"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper function"""
        self._redis.rpush(f"{method.__qualname__}:inputs", str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(f"{method.__qualname__}:outputs", str(output))
        return output

    return wrapper


def reply(fn: Callable) -> None:
    """display the history of calls of @fn"""
    r = redis.Redis()
    key = fn.__qualname__

    num_calls = r.get(key)
    try:
        num_calls = num_calls.decode('utf-8')
    except Exception:
        num_calls = 0

    print(f"{key} was called {num_calls} times:")

    inputs = r.lrange(f"{key}:inputs", 0, -1)
    outputs = r.lrange(f"{key}:outputs", 0, -1)

    for inp, out in zip(inputs, outputs):
        try:
            inp = inp.decode('utf-8')
        except Exception:
            inp = ""
        try:
            out = out.decode('utf-8')
        except Exception:
            out = ""
        print(f"Cache.store(*{inp}) -> {out}")


class Cache():
    """a class for using redis as a simple cache"""
    def __init__(self) -> None:
        """Init instance"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
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
