import os
from pymongo.server_api import ServerApi
from pymongo.mongo_client import MongoClient

mongodb_url = os.getenv('DB_URL')

# create a new client and connect to the server
CLIENT = MongoClient(mongodb_url, server_api=ServerApi('1'))

DB = CLIENT.get_database("fastapi__blog_api")

# collections
blogs_collection = DB.get_collection("blogs")
users_collection = DB.get_collection("users")
likes_collection = DB.get_collection("likes")

# send a ping to confirm a successful connection
try:
    CLIENT.admin.command('ping')
    print("App is successfully connected to the database mongoDB!")
except Exception as e:
    print(e)
