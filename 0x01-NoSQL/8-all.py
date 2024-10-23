#!/usr/bin/env python3
"""Python function to list all documents in a collection"""


def list_all(mongo_collection):
    """
    All documents in a collection are listed
    Return an empty list if no documnt is in the collection
    """
    documents = mongo_collection.find()
    if mongo_collection.count_documents({}) == 0:

        return []

    return list(documents)
