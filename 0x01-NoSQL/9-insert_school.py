#!/usr/bin/env python3
"""
    Python function that inserta  a new document in a collection
    based on Keyword arguments
"""

def insert_school(mongo_collection, **kwargs):
    """
    The Python collection object will be called 
    mongo_collection.  Returns the new _id.
    """
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id
