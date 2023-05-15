# Imports
import requests
import os
import json

from flask import Flask, render_template, request, jsonify, send_file, make_response
from flask.json import JSONEncoder
from bson.objectid import ObjectId
from datetime import datetime, timedelta
from dotenv import load_dotenv
from flask_cors import CORS

# Database
from assignment2cache.database import collection
from assignment2cache.database import collection2
from assignment2cache.database import client

# Parse functions
from assignment2cache.vcard_to_json_parser import vcard_parser
from assignment2cache.json_to_vcard_id_parser import json_id_parser

# Load dotenv
load_dotenv()

# Set the flask app
app = Flask(__name__)

# Make the app accept all requests
CORS(app, resources={r"/*": {"origins": "*"}})



# * POST route '/formcontacts' endpoint - Recieve the uploaded file from frontend and parses it to json. Add timestamp and push it to cacheAPI database (replace it of there already are data in it). Send the parsed file to mainAPI endpoint.
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
            'Content-Type': 'application/json',
            'X-API-Key': 'post-key'
        }

        # Make request
        res = requests.post(os.environ['MAIN_API'] + '/contacts', json=file_data, headers=headers)
        # Return request
        return res.json()



# * GET route '/contacts/vcard' (vcard) – Get the file from cacheApi database or mainAPI database, depending on id the cacheAPI got the requested data.
# * It also deletes everything in the collection after 10 days, to prevent buildup and loss of speed.  
@app.route('/contacts_cache/vcard', methods=['GET'])
def getVCardCache():

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
        
        # Set headers
        headers = {
            'X-API-Key': 'get-key'
        }   

        # Send request with headers
        res = requests.get(os.environ['MAIN_API'] + '/contacts/vcard', headers=headers)
       
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



# * GET route '/contacts_cache' endpoint - Show all contacts (json)
@app.route('/contacts_cache', methods=['GET'])
def getAllContactsCache():
    # Set headers
    headers = {
        'X-API-Key': 'get-key'
    }   
    # Send request with headers
    res = requests.get(os.environ['MAIN_API'] + '/contacts', headers=headers)
    
    # Return result
    return res.text


# * GET route '/contacts_cache/<id>' - Shows one contact based on id (json)
@app.route('/contacts_cache/<id>', methods=['GET'])
def getContactsCache(id):
    # Check if data based on id exists in cache database (collection vCard)
    cache_data_id = collection.find_one({"_id": ObjectId(id)})

    # If you fint id in database, then return it.
    if cache_data_id:
        return f'{cache_data_id}'

    # If not, get result from mainAPI
    else:
        # Set headers
        headers = {
            'X-API-Key': 'get-id-key'
        }   
        # Send request with headers
        res = requests.get(os.environ['MAIN_API'] + f'/contacts/{id}', headers=headers)
    
        # Return response
        return res.text


# * GET route '/contacts_cache/id/vcard' (vcard) – Parses one contact (based on id) in json back to vcf, and returns the parsed output.
@app.route('/contacts_cache/<id>/vcard', methods=['GET'])
def getVCardIdCache(id):
    # Check if data based on id exists in cache database (collection vCard_all)
    cache_data_id = collection2.find_one({"_id": ObjectId(id)})

    # If you find id in database, then return it.
    if cache_data_id:
        # Parse it
        json_id_parser(id)
        vcards_id_json = json_id_parser(id)
        # Return output
        return jsonify(vcards_id_json)

    # If you don't find id, then make request to mainAPI
    else:
        # Set headers
        headers = {
            'X-API-Key': 'get-id-key'
        }   
        # Send request with headers
        res = requests.get(os.environ['MAIN_API'] + f'/contacts/{id}/vcard', headers=headers)
    
        # Return response
        return res.text


# Run the cacheAPI app on port 3001
app.run(port=3001)
