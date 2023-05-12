from flask import Flask, render_template, request, jsonify, send_file, make_response
from flask.json import JSONEncoder
from bson.objectid import ObjectId
from datetime import datetime, timedelta
import os
import json
from dotenv import load_dotenv
from flask_cors import CORS
import requests

import database
from database import db
from database import collection
from database import collection2
from database import client
from vcard_to_json_parser import vcard_parser
from json_to_vcard_parser import json_parser
from json_to_vcard_id_parser import json_id_parser


load_dotenv()


# Set the flask app
app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})


# * HOME route – Render the HTML form to the page (kan slettes)
@app.route('/')
def test():
    return 'Hello world!'


# * Recieve the contact file from the frontend form, parse it to json and insert it into the cacheAPI database, and then send it further to the mainAPI.
@app.route('/formcontacts', methods=['POST'])
def formcontacts():

     # Retrive the uploaded file from the HTML form
    if request.method == 'POST':

        # Get the file
        uploaded_file = request.files.get('file')

        # If the file is NOT empty, do this:
        if uploaded_file.filename != '':
            uploaded_file.save(uploaded_file.filename)  # Saves the file
            vcard_parser(uploaded_file.filename)  # Parsing the file to JSON
            print(uploaded_file)
            os.remove(uploaded_file.filename)  # Remove the vcf file locally

    # Push the parsed file to the cacheAPI database (with timestamp)
    with open('data.json') as data:
        file_data = json.load(data)
        timestamp = datetime.utcnow()

        # If there are many instances, check timestamp and replace with new
        if isinstance(file_data, list):
            # Delete existing documents
            collection.delete_many({})
            # Insert new documents with timestamp
            documents = [dict(doc, timestamp=timestamp) for doc in file_data]
            collection.insert_many(documents)
        
        # If there are one instance, check timestamp and replace with new
        else:
            # Delete existing document
            collection.delete_one({})
            # Insert new document with timestamp
            document = dict(file_data, timestamp=timestamp)
            collection.insert_one(document)


    # Send the parsed file 'data.json' further to the mainAPI endpoint.
    with open('data.json') as data:
        # Get the file
        file_data = json.load(data)
        # Set headers
        headers = {
            'Content-Type': 'application/json'
        }
        # Make request
        res = requests.post(os.environ['MAIN_API'] + '/contacts', json=file_data, headers=headers)
        # Return request
        return res.json()



# * GET route '/contacts/vcard' (vcard) – Get the file from cacheApi database or mainAPI database, depending on id the cacheAPI got the requested data.
# * It also deletes everything in the collection after 10 days, to prevent buildup and loss of speed.  
@app.route('/contacts_cache/vcard', methods=['GET'])
def getVCard():

    # Check if data exists in cache database (the second collection (vCard_all))
    cache_data = list(collection2.find())

    # Create a TTL index that expires documents after 10 days
    collection2.create_index("timestamp", expireAfterSeconds=864000)

    # Query the cache collection to see if it has any expired documents
    expired_docs = collection2.find({"timestamp": {"$lt": datetime.utcnow() - timedelta(days=10)}})

    # Delete any expired documents from the cache collection
    for doc in expired_docs:
        collection2.delete_one({"_id": doc["_id"]})


    # If data is not found in cacheAPI database, get data from mainAPI 
    if not cache_data:
        res = requests.get(os.environ['MAIN_API'] + '/contacts/vcard')
       
        # Set the mainAPI data
        mainapi_data = res.json()
        # print('Backend data:', mainapi_data)

        # Put it inside the cache database
        if isinstance(mainapi_data, list):
            documents = [dict(doc, timestamp=datetime.utcnow()) for doc in mainapi_data]
            collection2.insert_many(documents)
        else:
            document = dict(mainapi_data, timestamp=datetime.utcnow())
            collection2.insert_one(document)
            cache_data = [document]

    # Convert ObjectId instances to string before serializing to JSON
    for doc in cache_data:
        if '_id' in doc:
            doc['_id'] = str(doc['_id'])

    # If the data exists in the cache database, return it to the user.
    else:
        return jsonify(cache_data)




# Run the app on port 3001
app.run(port=3001)
