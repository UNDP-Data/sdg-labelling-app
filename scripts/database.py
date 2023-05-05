from bson import ObjectId
from datetime import datetime, timedelta
import os
import pymongo

def get_document_collection():
    client = pymongo.MongoClient(os.getenv('MONGO_URI'))
    db = client[os.getenv('DBNAME')]
    collection = db[os.getenv('DOC_COLL')]
    return collection

def get_paragraph(doc_ids: list, recent_ids: list, language, email):
    mongo_collection = get_document_collection()
    pipeline = [
        # Replace null label arrays with empty arrays, so that the size operator is applied correctly
        {
            '$addFields': {
                'labels': {
                    '$ifNull': ['$labels', []]
                }
            }
        },
        # Filter out documents in the queue
        {
            '$match': {
                'language': language,
                '_id': {'$nin': [ObjectId(_id) for _id in recent_ids]},
                '$expr': {'$lte': [{'$size': '$labels'}, 2]}
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
        # Limit to first 100 documents
        {
            '$limit': 100
        }
    ]
    documents = list(mongo_collection.aggregate(pipeline))

    if documents:
        for doc in documents:
            doc['_id'] = str(doc['_id'])
            if doc['_id'] not in doc_ids and doc['_id'] not in recent_ids and not check_user_email(doc, email):
                update_queue(doc['_id'])
                doc_ids.append(doc['_id'])
                return doc, doc_ids, recent_ids

    raise Exception('No documents found')

def check_user_email(doc, email):
    for user in doc['labels']:
        if user['email'] == email:
            return True
    return False

def get_recent_ids():
    collection = get_document_collection()
    docs = collection.find(
        {'date': {'$gt': datetime.now() - timedelta(minutes=10)}}, {'_id': 1})
    return [str(doc['_id']) for doc in docs]

def update_queue(_id):
    collection = get_document_collection()
    collection.update_one({'_id': ObjectId(_id)}, {"$set": {'date': datetime.now()}}, upsert=True)

def update_paragraph(_id, labels, email):
    _id = ObjectId(_id)
    collection = get_document_collection()
    document = collection.find_one({'_id': _id})

    if document:
        if document['labels'] != None:
            aux = list(document['labels'])
            flag = False
            i = 0
            while i < len(aux) and not flag:
                if aux[i]['email'] == email:
                    flag = True
                    aux[i]['user_labels'] = [label+1 for label in labels]
                i += 1
            if not flag:
                aux.append({'email': email, 'user_labels': [label+1 for label in labels]})
            document['labels'] = aux
            collection.replace_one({'_id': _id}, document)
        else:
            document['labels'] = [{'email' : email, 'user_labels' : [label+1 for label in labels]}]
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
