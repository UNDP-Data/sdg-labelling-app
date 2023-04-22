from bson import ObjectId
from dotenv import load_dotenv
import os 
import pymongo

def get_document_collection():
    load_dotenv()
    x = os.getenv('MONGO_URI')
    client = pymongo.MongoClient(os.getenv('MONGO_URI'))
    db = client['sdg_text_corpora']
    collection = db['test']
    return collection


def get_paragraphs(mongo_collection):
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
        # Sort by count in ascending order
        {
            '$sort': { 'count': 1 }
        },
        # Limit to first 300 documents
        {
            '$limit': 300
        }
    ]
    documents = list(mongo_collection.aggregate(pipeline))

    if documents:
        for doc in documents:
            doc['_id'] = str(doc['_id'])
        return documents
    else:
        raise Exception('No documents found')
    

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