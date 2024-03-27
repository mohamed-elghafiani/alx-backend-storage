#!/usr/bin/env python3
"""Log stats"""
from pymongo import MongoClient


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')

    logs = client.logs.nginx

    print(f"{logs.count_documents({})} logs")

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print("Methods:")
    for method in methods:
        print(f"\tmethod {method}:", logs.count_documents({ "method": method }))

    print(logs.count_documents({ "method": "GET", "path": "/status" }), "status check")

    print('IPs:')
    pipe = [
            {'$group': {'_id': '$ip', 'count': {'$sum': 1}}},
            {'$sort': {'count': -1}},
            {'$limit': 10}
    ]
    popular = list(logs.aggregate(pipe))
    for ip in popular:
        print('\t{}: {}'.format(ip['_id'], ip['count']))
