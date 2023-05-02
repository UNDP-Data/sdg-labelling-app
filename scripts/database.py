from bson import ObjectId
from datetime import datetime, timedelta
import os 
import pymongo

def get_document_collection():
    client = pymongo.MongoClient(os.getenv('MONGO_URI'))
    db = client['sdg_text_corpora']
    collection = db['test']
    return collection


def get_paragraph(mongo_collection, doc_ids : list):
    pipeline = [
        # Filter out documents with null labels
        {
            '$match': {
                'labels': { '$ne': None },
                '$expr': { '$lte': [{ '$size': '$labels' }, 2] }
            }
        },
        # Add a count field to each document
        {
            '$addFields': {
                'count': { '$size': '$labels' }
            }
        },
        # Sort by count in descending order
        {
            '$sort': { 'count': -1 }
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
            if doc['_id'] not in doc_ids and check_queue(doc['_id']):
                update_queue(doc['_id'])
                doc_ids.append(doc['_id'])
                return doc, doc_ids
    
    raise Exception('No documents found')
    
def update_queue(_id):
    client = pymongo.MongoClient(os.getenv('MONGO_URI'))
    db = client['sdg_text_corpora']
    collection = db['paragraph_queue']

    doc = collection.find_one({'_id': _id})
    if doc:
        collection.replace_one({'_id': _id}, {'_id' : _id, 'date' : datetime.now()})
    else:
        collection.insert_one({'_id' : _id, 'date' : datetime.now()})

def check_queue(_id):
    client = pymongo.MongoClient(os.getenv('MONGO_URI'))
    db = client['sdg_text_corpora']
    collection = db['paragraph_queue']
    doc = collection.find_one({'_id' : _id})
    
    if doc:
        if datetime.now() - doc['date'] >= timedelta(hours=1):
            return True
        return False
    else:
        return True
        


def update_paragraph(collection, _id, labels): 
    _id = ObjectId(_id)
    document = collection.find_one({'_id': _id})

    if document:
        document['labels'] += [labels]
        collection.replace_one({'_id': _id}, document)
    else :
        raise Exception('Document not found')


def get_paragraph_by_id(collection, _id):
    _id = ObjectId(_id)
    document = collection.find_one({'_id': _id})
    if document:
        document['_id'] = str(document['_id'])
        return document
    else:
        raise Exception('Document not found')