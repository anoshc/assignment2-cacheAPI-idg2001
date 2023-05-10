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
from vcard_to_json_parser import vcard_parser

load_dotenv()

# Set the flask app
app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})


# * HOME route – Render the HTML form to the page
@app.route('/')
def test():
    return 'Hello world!'


# * Recieve the contact file from the frontend form
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


# * En GET request som henter ferdig parset fil fra cache databasen, men om den ikke finst i cache db, hent filen fra backend(main api).

    # 1. Får en GET request fra frontend
    # 2. Sjekker om chache db har filen frontend trenger
    # 3. Viss ikke, hent filen fra backend
    # 4. Push GET requesten til frontenden

# * GET route '/contacts' endpoint - Show all contacts (json)
@app.route('/contacts_cache', methods=['GET'])
def getAllContacts():
     # Get all the documents from the collection
    all_contacts = list(collection.find({}))
    # Convert ObjectId to string and remove _id field from each document
    return jsonify(all_contacts)


# ! Dette er fra main-api, men måtte være i cachen også. Usikker om vi må endre disse eller ikke (evt sjekke om det fins i cahce-db, eller om man må hente fra main-api.)
# * GET route '/contacts/<id>' - Shows one contact based on id (json)
# @app.route('/contacts_cache/<id>', methods=['GET'])
# def getContacts(id):
    # result = collection.find_one({"_id": ObjectId(id)})
    # return f'{result}'


# * GET route '/contacts/vcard' (vcard) – Parses the contacts in json back to vcf, and shows all contacts in vcf.
# @app.route('/contacts_cache/vcard', methods=['GET'])
# def getVCard():
    #json_parser()  # Runs when we type in the route in Postman
    #vcards_json = json_parser()
    #return jsonify(vcards_json) # Pushes the json to the Postman output


# * GET route '/contacts/id/vcard' (vcard) – Parses one contact (based on id) in json back to vcf, and shows that one contact in vcf.
# @app.route('/contacts_cache/<id>/vcard', methods=['GET'])
# def getVCardId(id):
    # json_id_parser(id)
    # vcards_id_json = json_id_parser(id)
    # return jsonify(vcards_id_json)


# Run the app on port 3001
app.run(port=3001)
