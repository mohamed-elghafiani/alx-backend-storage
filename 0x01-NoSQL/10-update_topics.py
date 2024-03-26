#!/usr/bin/env python3
"""Update a document in Python"""


def update_topics(mongo_collection, name, topics):
    """Changes all topics of documents in @mongo_collection based on the name"""
    filter_by = { "name": name }
    update = { "$set": { "topics": topics } }
    mongo_collection.update_one(filter_by, update)
