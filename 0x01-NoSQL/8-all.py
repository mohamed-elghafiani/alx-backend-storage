#!/usr/bin/env python3
"""List documents in a collection"""


def list_all(mongo_collection):
    """Returns list of documents in @mongo_collection"""
    return mongo_collection.find()
