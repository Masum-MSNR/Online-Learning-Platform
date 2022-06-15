from pymongo import MongoClient
client = MongoClient(
    'mongodb+srv://masum:masum@cluster0.9cl0s.mongodb.net/test?retryWrites=true&w=majority')
db = client.onlinelearning
