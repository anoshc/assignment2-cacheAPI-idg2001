from flask import Flask, render_template, request, jsonify, send_file, make_response
from bson.objectid import ObjectId
import os
import json
from dotenv import load_dotenv
from flask_cors import CORS
import requests

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



# * GET route '/contacts/vcard' (vcard) – Get the file from cache db or main-api.
#! Vet ikke om den funker ennå.
@app.route('/contacts_cache/vcard', methods=['GET'])
def getVCard():
    # # Check if requested vcard exists in cache database
    # vcard = list(collection.find())
    # if vcard:
    #     # If vcard is found in cache, return it
    #     return f' {(list(vcard))}'
    # else:
    # If vcard is not found in cache, get it from main-api
    res = requests.get(os.environ['MAIN_API'] + '/contacts/vcard')
    vcard_data = res.text
    print(vcard_data)
    # Save vcard to cache database
    collection.insert_one({'name': 'vcard', 'data': vcard_data})

    # Return vcard data
    return vcard_data

'''
1. Må legge til at cachen skal lagre det den får fra backend (vcard filen) i cahce-databasen også. 
2. Og vi må legge til en if-statement som sjekker om det brukeren spør om finnes i cache-databasen,
    så send det til frontend, viss ikke så må den må hente det fra backend-databasen,
    lagre i cahcen, og igjen sende til frontend.
'''


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
