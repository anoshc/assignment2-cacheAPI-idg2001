import os
import certifi
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
MONGO_COLLECTION2_NAME = os.environ['MONGO_COLLECTION2_NAME']

client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
db = client[MONGO_DB_NAME]
collection = db[MONGO_COLLECTION_NAME]
collection2 = db[MONGO_COLLECTION2_NAME]
