# standard library
import os
from random import choice
from datetime import datetime, timedelta

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


def get_paragraph(config: entities.SessionConfig):
    collection = get_document_collection()
    pipeline = [
        # Find matching documents
        {
            '$match': {
                # match text langauge
                'language': config.language,

                # exclude texts labelled by the user
                'annotations': {'$not': {'$elemMatch': {'created_by': config.user_id}}},

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
        # $sample in Azure Cosmos DB for MongoDB vCore currently has unexpected behaviour
        # {
        #     '$sample': {'size': 1},
        # }
    ]

    docs = list(collection.aggregate(pipeline))
    if not docs:
        return None
    doc = choice(docs)
    # "hide" the text from being shown to other labellers for the duration specified in timedelta above
    collection.update_one({'_id': doc['_id']}, {'$set': {'retrieved_at': datetime.utcnow()}})
    doc['_id'] = str(doc['_id'])
    return doc


def update_paragraph(_id, annotation: entities.Annotation):
    collection = get_document_collection()
    to_filter = {
        '_id': ObjectId(_id),
        'annotations': {'$elemMatch': {'created_by': annotation.created_by}},
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
                'annotations.$.created_at': annotation.created_at,
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


def get_stats_by_language() -> dict:
    collection = get_document_collection()
    pipeline = [
        {
            '$group': {
                '_id': '$language',
                'count': {
                '$sum': {'$size': '$annotations'}
                }
            }
        },
        {
            '$project': {
                '_id': 0,
                'language': '$_id',
                'count': 1
            }
        },
    ]
    stats = {
        doc['language']: doc['count'] / int(os.environ['PER_LANGUAGE_GOAL']) * 100
        for doc in collection.aggregate(pipeline)
    }
    return stats


def get_stats_user(config) -> int:
    collection = get_document_collection()
    count = collection.count_documents({'annotations': {'$elemMatch': {'created_by': config.user_id}}})
    return count
