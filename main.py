from flask import Flask, render_template, request, jsonify, send_file, make_response
from bson.objectid import ObjectId
import os
import json

from database import db
from database import collection
from database import client

# Set the flask app
app = Flask(__name__)


# * HOME route – Render the HTML form to the page
@app.route('/')
def test():
    return 'Hello world!'


# * Recieve the contact file from the frontend form, må denne være en POST eller GET?
@app.route('/formcontacts', methods=['POST'])
def formcontacts():
    # Retrive the uploaded file from the html form
    if request.method == 'POST':
        uploaded_file = request.files['file']
        # If the file is NOT empty, do this:
        if uploaded_file.filename != '':
            uploaded_file.save(uploaded_file.filename)  # Saves the file
            os.remove(uploaded_file.filename)  # Remove the vcf file locally
            return 'File read successfully and uploaded to database!'
        else:
            return 'Could not read file, try again.'  # In case of error

    # Push the uploaded file to the database
    with open(uploaded_file) as data:
        uploaded_file = json.load(data)
        if isinstance(uploaded_file, list):
            collection.insert_many(uploaded_file)
        else:
            collection.insert_one(uploaded_file)
        return uploaded_file

    # En funksjonalitet som sender 'uploaded file' to backend (main api)


# * En GET request som henter ferdig parset fil fra cache databasen, men om den ikke finst i cache db, hent filen fra backend(main api).

    # 1. Får en GET request fra frontend
    # 2. Sjekker om chache db har filen frontend trenger
    # 3. Viss ikke, hent filen fra backend
    # 4. Push GET requesten til frontenden

# * GET route '/contacts' endpoint - Show all contacts (json)
@app.route('/contacts_cache', methods=['GET'])
def getAllContacts():
    result = collection.find()
    return f' {(list(result))}'


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
