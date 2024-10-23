#1/usr/bin/env python3
"""
   Python program returns the list of schools with a specific topic.
"""

def schools_by_topic(mongo_collection, topic):
    """
    mongo_collection will be the pymongo collection object, and the 
    topic (string) will be searched.
    """
    documents = mongo_collection.find({"topics": topic})
    list_docs = [i for i in documents]
    return list_docs
