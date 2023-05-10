from flask import Flask, render_template, request, jsonify, send_file, make_response

from database import db
from database import collection
from database import client

# Set the flask app
app = Flask(__name__)

'''
1. Skal få contact filen fra frontend og sende den videre til backend(main api) i en POST request. 
   Skal også lagres i cach-databasen.

2. Frontend sender en GET request av den ferdig parset filen i backend.
   Da må cachen sjekke om den har filen lokalt, viss ikke, så må den hente filen fra backend(main api) POST?.

3. 
'''



# * HOME route – Render the HTML form to the page
@app.route('/')
def test():
    return 'Hello world!'


# * Recieve the contact file from the frontend form, må denne være en POST eller GET?
@app.route('/formcontacts', method=['POST'])
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
            return 'Could not read file, try again.' # In case of error

    # Push the uploaded file to the database
    with open(uploaded_file) as data:
        uploaded_file = json.load(data)
        if isinstance(uploaded_file, list):
            collection.insert_many(uploaded_file)
        else:
            collection.insert_one(uploaded_file)
        return uploaded_file


# * En ny POST request som sender 'uploaded file' to backend (main api)



# * En GET request som henter ferdig parset fil fra cache databasen, men om den ikke finst i cache db, hent filen fra backend(main api).


# * En POST request som tar den filen vi hentet fra cache db eller backend(main api), og sender til frontend


# Run the app on port 3001
app.run(port=3001)