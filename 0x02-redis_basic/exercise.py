#!/usr/bin/env python3
""" A module designed to use Redis Nosql data Storage """

import redis
from typing import Union, Optional, Callable
from uuid import uuid4, UUID
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Tracks how many times a method in a Cache class is called.
    """

    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Invokes the specified method after increasing its call counter.
        """
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """ Decorator to store the history of inputs and
    outputs for a particular function.
    """

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ Wrapper for decorator functionality """
        input = str(args)
        self._redis.rpush(method.__qualname__ + ":inputs", input)

        output = str(method(self, *args, **kwargs))
        self._redis.rpush(method.__qualname__ + ":outputs", output)

        return output

    return wrapper


def replay(method: Callable):
    """ display the history of calls of a particular function """
    key = method.__qualname__
    inputs = key + ":inputs"
    outputs = key + ":outputs"
    redis = method.__self__._redis
    count = redis.get(key).decode("utf-8")
    print("{} was called {} times:".format(key, count))
    inputList = redis.lrange(inputs, 0, -1)
    outputList = redis.lrange(outputs, 0, -1)
    redis_zipped = list(zip(inputList, outputList))
    for a, b in redis_zipped:
        attr, data = a.decode("utf-8"), b.decode("utf-8")
        print("{}(*{}) -> {}".format(key, attr, data))


class Cache:
    """ Class to implement a Cache """

    def __init__(self):
        """ Constructor Method """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store the input data in Redis using a
        random key and return the key.
        """
        random_key = str(uuid4())
        self._redis.set(random_key, data)

        return random_key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """ Reading from Redis and recovering original data type"""
        value = self._redis.get(key)
        if fn:
            value = fn(value)

        return value

    def get_str(self, key: str) -> str:
        """ Parameterizes a value from redis to str """
        value = self._redis.get(key)
        return value.decode("utf-8")

    def get_int(self, key: str) -> int:
        """An integer value from a redis data storage is retrieved"""
        value = self._redis.get(key)
        try:
            value = int(value.decode("utf-8"))
        except Exception:
            value = 0
        return value
