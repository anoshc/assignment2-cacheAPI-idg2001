import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Loading env variables
load_dotenv()

# Finding connection string
# mongo_url = os.environ.get('MONGO_URL')

# Get variables from Render
MONGO_URI = os.environ['MONGO_URI']
MONGO_DB_NAME = os.environ['MONGO_DB_NAME']
MONGO_COLLECTION_NAME = os.environ['MONGO_COLLECTION_NAME']

client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]
collection = db[MONGO_COLLECTION_NAME]