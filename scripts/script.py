def getParagraphs(mongo_collection):
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
    return list(mongo_collection.aggregate(pipeline))
    

def updateParagraph(collection, _id, labels): 
    document = collection.find_one({'_id': _id})

    if document:
        document['labels'] += [labels]
        print(document['labels'])
        collection.replace_one({'_id': _id}, document)
        print(collection.find_one({'_id': _id}))
    else :
        print ('Document not found')


def getParagraphById(collection, _id):
    document = collection.find_one({'_id': _id})
    return document