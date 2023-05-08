# standard library
import os
from datetime import datetime, timedelta

# database
import pymongo
from bson import ObjectId


def get_document_collection():
    client = pymongo.MongoClient(os.getenv('MONGO_URI'))
    db = client[os.getenv('DBNAME')]
    collection = db[os.getenv('DOC_COLL')]
    return collection


def get_paragraph(language, email):
    collection = get_document_collection()
    pipeline = [
        # Replace null label arrays with empty arrays, so that the size operator is applied correctly
        {
            '$addFields': {
                'annotations': {
                    '$ifNull': ['$annotations', []]
                },
                'retrieved_at': {
                    '$ifNull': ['$retrieved_at', datetime(2023, 1, 1)]
                }
            }
        },
        # Find matching documents
        {
            '$match': {
                'language': language,  # match text langauge
                'annotations': {'$not': {'$elemMatch': {'email': email}}},  # exclude texts labelled by the user
                'retrieved_at': {'$lte': datetime.now() - timedelta(minutes=10)},  # exclude texts that have just been labelled
                '$expr': {'$lte': [{'$size': '$annotations'}, 2]}  # exclude texts with already 3 annotations
            }
        },
        # Add a count field to each document
        {
            '$addFields': {
                'count': {'$size': '$annotations'}
            }
        },
        # Sort by count in descending order
        {
            '$sort': {'count': -1}
        },
        {
            '$sample': {'size': 1},
        }
    ]

    docs = list(collection.aggregate(pipeline))
    if not docs:
        return None
    doc = docs[0]
    doc['_id'] = str(doc['_id'])
    update_queue(_id=doc['_id'])
    return doc


def update_queue(_id):
    collection = get_document_collection()
    collection.update_one({'_id': ObjectId(_id)}, {'$set': {'retrieved_at': datetime.now()}})


def update_paragraph(_id, labels, email):
    collection = get_document_collection()
    _id = ObjectId(_id)
    doc = collection.find_one({'_id': _id}, {'annotations': 1})
    to_filter = {
        '_id': _id,
        'annotations': {'$elemMatch': {'email': email}},
    }
    to_update = {
        '$set': {'annotations.$.labels': labels},
    }
    for annotation in doc.get('annotations', list()):
        if annotation['email'] == email:
            result = collection.update_one(to_filter, to_update)
            break
    else:
        to_filter.pop('annotations')
        to_update = {
            '$push': {'annotations': {'email': email, 'labels': labels}},
        }
        result = collection.update_one(to_filter, to_update)
    return result.upserted_id


def get_paragraph_by_id(_id):
    _id = ObjectId(_id)
    collection = get_document_collection()
    document = collection.find_one({'_id': _id})
    if document:
        document['_id'] = str(document['_id'])
        return document
    else:
        raise Exception('Document not found')
