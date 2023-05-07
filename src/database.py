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
                'labels': {
                    '$ifNull': ['$labels', []]
                }
            }
        },
        # Find matching documents
        {
            '$match': {
                'language': language,  # match text langauge
                'labels': {'$not': {'$elemMatch': {'email': email}}},  # exclude texts labelled by the user
                'date': {'$lte': datetime.now() - timedelta(minutes=10)},  # exclude texts that have just been labelled
                '$expr': {'$lte': [{'$size': '$labels'}, 2]}  # exclude texts with already 3 labels
            }
        },
        # Add a count field to each document
        {
            '$addFields': {
                'count': {'$size': '$labels'}
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
    if docs:
        doc = docs[0]
        doc['_id'] = str(doc['_id'])
        return doc
    raise Exception('No documents found')


def update_queue(_id):
    collection = get_document_collection()
    collection.update_one({'_id': ObjectId(_id)}, {'$set': {'date': datetime.now()}}, upsert=True)


def update_paragraph(_id, labels, email):
    _id = ObjectId(_id)
    collection = get_document_collection()
    document = collection.find_one({'_id': _id})

    if document:
        if document.get('labels'):
            aux = list(document['labels'])
            flag = False
            i = 0
            while i < len(aux) and not flag:
                if aux[i]['email'] == email:
                    flag = True
                    aux[i]['user_labels'] = labels
                i += 1
            if not flag:
                aux.append({'email': email, 'user_labels': labels})
            document['labels'] = aux
            collection.replace_one({'_id': _id}, document)
        else:
            document['labels'] = [{'email': email, 'user_labels': labels}]
            collection.replace_one({'_id': _id}, document)
    else:
        raise Exception('Document not found')


def get_paragraph_by_id(_id):
    _id = ObjectId(_id)
    collection = get_document_collection()
    document = collection.find_one({'_id': _id})
    if document:
        document['_id'] = str(document['_id'])
        return document
    else:
        raise Exception('Document not found')
