#!/usr/bin/env python3
""" Main file """

Cache = __import__('exercise').Cache
reply = __import__('exercise').reply

cache = Cache()

s1 = cache.store("first")
s2 = cache.store("secont")
s3 = cache.store("third")

reply(cache.store)
