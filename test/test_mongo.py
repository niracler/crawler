import pymongo

client = pymongo.MongoClient('mongodb://root:123456@10.42.30.245:27017/')
db = client['test']
collection = db['students']
student = {
    'id': '20170101',
    'name': 'Jordan',
    'age': 20,
    'gender': 'male'
}
result = collection.insert_one(student)
print(result.inserted_id)
