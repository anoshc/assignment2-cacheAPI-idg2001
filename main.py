from flask import Flask, render_template, request, jsonify, send_file, make_response
from bson.objectid import ObjectId
import os
import json
from dotenv import load_dotenv
from flask_cors import CORS
import requests
import hashlib

import database
from database import db
from database import collection
from database import client

load_dotenv()

# Set the flask app
app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})


# * HOME route – Render the HTML form to the page (kan slettes)
@app.route('/')
def test():
    return 'Hello world!'


# * Recieve the contact file from the frontend form and send it to main-api
@app.route('/formcontacts', methods=['POST'])
def formcontacts():

    #print('formcontacts')
    
    # Retrieve and set the uploaded file
    uploaded_file = request.files['file']
    #print(uploaded_file)

    # Read the uploaded file
    f = uploaded_file.read()
    # See the uploaded file in the console
    print(f) 

    # Send the uploaded file to the main api endpoint
    res = requests.post(os.environ['MAIN_API'] + '/contacts', files={'file': f})

    return res.text 



# * GET route '/contacts/vcard' (vcard) – Get the file from cacheApi database or mainAPI database, depending on id the cacheAPI got the requested data.
@app.route('/contacts_cache/vcard', methods=['GET'])
def getVCard():
    # Check if data exists in cache database
    cache_data = list(collection.find())  

    # Initialize hash variables
    cache_hash = ''
    backend_hash = ''

    # If there is data in the cache database
    if cache_data:
        # Get the hashing and data
        cache_data = cache_data[0]
        cache_hash = cache_data.get('hash', '')
        cache_data = cache_data.get('data', '')
        
        # Checks whether the cache_data retrieved from the cache database is not empty, and whether its hash value matches the hash value calculated using the hashlib library's sha256 algorithm.
        if cache_data and cache_hash == hashlib.sha256(cache_data.encode()).hexdigest():
            print ('Cache data: ' + cache_data)
            
            # Then check if the backend_hash match with the catch_hash
            if backend_hash != cache_hash:

                # If data not found in cache or the hash doesn't match, get data from backend
                res = requests.get(os.environ['MAIN_API'] + '/contacts/vcard')
                backend_data = res.text
                print('Backend data:' + backend_data)

                # Calculate hash of data from backend
                backend_hash = hashlib.sha256(backend_data.encode()).hexdigest()
                
                # Remove old data from cacheAPI database
                collection.delete_many({'name': 'vcard'})

                # Save new data and hash to cacheAPI database
                collection.insert_one({'name': 'vcard', 'data': backend_data, 'hash': backend_hash})

                # Return data from backend to the frontend
                return backend_data
            
            else:
                # If the backend_hash and cache_hash matches, then return data from cacheAPI database
                return cache_data



# # * GET route '/contacts_cache/<id>' - Shows one contact based on id (json)
# @app.route('/contacts_cache/<id>', methods=['GET'])
# def getContacts(id):
#     # Check cache database first
#     result = collection.find_one({"_id": ObjectId(id)})
#     if result:
#         return f'{result}'
    
#     # If not found in cache, fetch from main API
#     res = requests.get(f'{os.environ["MAIN_API"]}/contacts/{id}')
#     data = res.text
    
#     # Save to cache database
#     collection.insert_one({'_id': ObjectId(id), 'data': data})
    
#     # Return the fetched data
#     return data


# # * GET route '/contacts_cache/vcard' (vcard) – Parses the contacts in json back to vcf, and shows all contacts in vcf.
# @app.route('/contacts_cache/vcard', methods=['GET'])
# def getVCard():
#     # Check cache database first
#     result = collection.find_one({'name': 'vcard'})
#     if result:
#         return jsonify(result['data'])
    
#     # If not found in cache, fetch from main API and parse to vcard format
#     res = requests.get(f'{os.environ["MAIN_API"]}/contacts/vcard')
#     vcard_data = json_parser(res.text)
    
#     # Save to cache database
#     collection.insert_one({'name': 'vcard', 'data': vcard_data})
    
#     # Return the parsed vcard data
#     return jsonify(vcard_data)


# # * GET route '/contacts_cache/id/vcard' (vcard) – Parses one contact (based on id) in json back to vcf, and shows that one contact in vcf.
# @app.route('/contacts_cache/<id>/vcard', methods=['GET'])
# def getVCardId(id):
#     # Check cache database first
#     result = collection.find_one({'name': f'vcard-{id}'})
#     if result:
#         return jsonify(result['data'])
    
#     # If not found in cache, fetch from main API and parse to vcard format
#     res = requests.get(f'{os.environ["MAIN_API"]}/contacts/{id}/vcard')
#     vcard_data = json_id_parser(res.text)
    
#     # Save to cache database
#     collection.insert_one({'name': f'vcard-{id}', 'data': vcard_data})
    
#     # Return the parsed vcard data
#     return jsonify(vcard_data)


# Run the app on port 3001
app.run(port=3001)
