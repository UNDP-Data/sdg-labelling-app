# standard library
import os
from datetime import datetime, timedelta
from collections import namedtuple

# database
import pymongo
from bson import ObjectId


def get_document_collection():
    client = pymongo.MongoClient(os.environ['MONGO_URI'])
    db = client[os.environ['DATABASE_NAME']]
    collection = db[os.environ['COLLECTION_NAME']]
    return collection


def read_sdg_metadata():
    client = pymongo.MongoClient(os.environ['MONGO_URI'])
    db = client[os.environ['DATABASE_NAME']]
    collection = db['sdgs']
    doc = collection.find_one({}, {'_id': 0})
    SDG = namedtuple('SustainableDevelopmentGoal', doc)
    sdgs = [SDG(**sdg) for sdg in collection.find({}, {'_id': 0})]
    return sdgs


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
                # match text langauge
                'language': language,

                # exclude texts labelled by the user
                'annotations': {'$not': {'$elemMatch': {'email': email}}},

                # exclude texts that have just been labelled to avoid getting more annotations than required
                'retrieved_at': {'$lte': datetime.now() - timedelta(minutes=10)},

                # exclude texts with already 3 annotations
                '$expr': {'$lt': [{'$size': '$annotations'}, int(os.environ['MAX_ANNOTATIONS'])]}
            }
        },
        # Add a count field to each document
        {
            '$addFields': {
                'count': {'$size': '$annotations'}
            }
        },
        # sample from top n examples by annotation count
        {
            '$sort': {'count': -1}
        },
        {
            '$limit': 100,
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


def update_paragraph(_id, labels, email, comment):
    collection = get_document_collection()
    _id = ObjectId(_id)
    doc = collection.find_one({'_id': _id}, {'annotations': 1})
    to_filter = {
        '_id': _id,
        'annotations': {'$elemMatch': {'email': email}},
    }
    to_update = {
        '$set': {
            'annotations.$.labels': labels,
            'annotations.$.comment': comment,
        },
    }
    for annotation in doc.get('annotations', list()):
        if annotation['email'] == email:
            result = collection.update_one(to_filter, to_update)
            break
    else:
        to_filter.pop('annotations')
        to_update = {
            '$push': {'annotations': {'email': email, 'labels': labels, 'comment': comment}},
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
