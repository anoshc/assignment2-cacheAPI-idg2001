from flask import Flask, render_template, request, jsonify, send_file, make_response

# Set the flask app
app = Flask(__name__)

# * HOME route – Render the HTML form to the page
@app.route('/')
def test():
    return 'Hello world!'

# Run the app on port 3001
app.run(port=3001)