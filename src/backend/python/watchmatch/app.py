from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd

from search.search import search

app = Flask(__name__)
CORS(app)

@app.route('/search/<given_watch>', methods=['GET'])
def search_api(given_watch):
    results = search(given_watch)
    return jsonify(results)

if __name__ == "__main__":
    app.run(host='localhost', port=5000)