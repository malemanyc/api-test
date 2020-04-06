import os
import sys
import shelve
import markdown
import parsestring
from flask import Flask, jsonify, request, g

# Createan a Flask instance
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST']) 
def index():
    """ 
    GET:Present documentation.
    POST: Send some raw string and obtain json format of all names contained.
    """

    if request.method == 'POST':
        # Capture raw input string
        input_string = request.data

        # Process input string
        data = parsestring.process_str(str(input_string))

        # Return  json data
        return jsonify(data), 201

    # When request method is GET
    else:

        # Open documentation file
        with open(os.path.dirname(app.root_path) + '/README.md', 'rt') as doc_file:
            # Read documentation file
            content = doc_file.read()

            # Convert to HTML
            return markdown.markdown(content)
