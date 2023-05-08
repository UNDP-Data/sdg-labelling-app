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
    if docs:
        doc = docs[0]
        doc['_id'] = str(doc['_id'])
        return doc
    raise Exception('No documents found')


def update_queue(_id):
    collection = get_document_collection()
    collection.update_one({'_id': ObjectId(_id)}, {'$set': {'retrieved_at': datetime.now()}}, upsert=True)


def update_paragraph(_id, labels, email):
    _id = ObjectId(_id)
    collection = get_document_collection()
    document = collection.find_one({'_id': _id})

    if document:
        if document.get('annotations'):
            aux = list(document['annotations'])
            flag = False
            i = 0
            while i < len(aux) and not flag:
                if aux[i]['email'] == email:
                    flag = True
                    aux[i]['labels'] = labels
                i += 1
            if not flag:
                aux.append({'email': email, 'labels': labels})
            document['annotations'] = aux
            collection.replace_one({'_id': _id}, document)
        else:
            document['annotations'] = [{'email': email, 'labels': labels}]
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
