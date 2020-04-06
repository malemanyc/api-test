import os
import sys
import shelve
import markdown
import parsestring
from flask import Flask, jsonify, request, g

# Createan a Flask instance
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST']) #converts the index method into an url endpoint?
def index():
    """Present documentation. """
    if request.method == 'POST':
        input_string = request.data
        data = parsestring.process_str(str(input_string))
        return jsonify(data), 201
    else:
        with open(os.path.dirname(app.root_path) + '/README.md', 'rt') as doc_file:
            # Read documentation file
            content = doc_file.read()
            # Convert to HTML
            return markdown.markdown(content)


@app.route('/test1/<int:num>', methods=['GET']) # if you don't specify method, default is GET
def get_multiply10(num):
	return jsonify({'result': num*10})
