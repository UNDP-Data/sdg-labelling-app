from bson import ObjectId

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

    for doc in documents:
        doc['_id'] = str(doc['_id'])
    
    return documents
    

def update_paragraph(collection, _id, labels): 
    _id = ObjectId(_id)
    document = collection.find_one({'_id': _id})

    if document:
        document['labels'] += [labels]
        print(document['labels'])
        collection.replace_one({'_id': _id}, document)
        print(collection.find_one({'_id': _id}))
    else :
        print ('Document not found')


def get_paragraph_by_id(collection, _id):
    _id = ObjectId(_id)
    document = collection.find_one({'_id': _id})
    if document:
        document['_id'] = str(document['_id'])
        return document
    else:
        print('Document not found')