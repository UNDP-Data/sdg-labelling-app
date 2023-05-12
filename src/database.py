# standard library
import os
from datetime import datetime, timedelta
from collections import namedtuple

# database
import pymongo
from bson import ObjectId

# local packages
from src import entities


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


def get_paragraph(config: entities.Config):
    collection = get_document_collection()
    pipeline = [
        # Find matching documents
        {
            '$match': {
                # match text langauge
                'language': config.session_language,

                # exclude texts labelled by the user
                'annotations': {'$not': {'$elemMatch': {'email': config.session_email}}},

                # exclude texts that have just been labelled to avoid getting more annotations than required
                'retrieved_at': {'$lte': datetime.utcnow() - timedelta(minutes=10)},

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
    # "hide" the text from being shown to other labellers for the duration specified in timedelta above
    collection.update_one({'_id': doc['_id']}, {'$set': {'retrieved_at': datetime.now()}})
    doc['_id'] = str(doc['_id'])
    return doc


def update_paragraph(_id, annotation: entities.Annotation):
    collection = get_document_collection()
    to_filter = {
        '_id': ObjectId(_id),
        'annotations': {'$elemMatch': {'email': annotation.email}},
    }
    document = collection.find_one(to_filter, {'_id': 1})
    if document is None:
        to_filter.pop('annotations')
        to_update = {
            '$push': {'annotations': annotation.dict()},
        }
    else:
        to_update = {
            '$set': {
                'annotations.$.labels': annotation.labels,
                'annotations.$.comment': annotation.comment,
            },
        }
    result = collection.update_one(to_filter, to_update)
    return result.upserted_id


def get_paragraph_by_id(_id):
    collection = get_document_collection()
    document = collection.find_one({'_id': ObjectId(_id)})
    if document:
        document['_id'] = str(document['_id'])
    return document
