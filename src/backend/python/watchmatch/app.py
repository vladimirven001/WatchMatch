from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd

from search.search import search
from matchmaker.watchMatch import watch_match_cosine

app = Flask(__name__)
CORS(app)

@app.route('/search/<given_watch>', methods=['GET'])
def search_api(given_watch):
    results = search(given_watch)
    return jsonify(results)

@app.route('/match/<given_watch>', methods=['GET'])
def search_match_api(given_watch):
    try:
        filters = request.args.get('filters')
    except Exception as e:
        print(e)
        filters = {"excludedBrands":[],"minPrice":"","maxPrice":"","excludedCaseMaterials":[],"excludedDialColors":[]}
    results = watch_match_cosine(given_watch=given_watch, filters=filters)
    print(results)
    return jsonify(results)

if __name__ == "__main__":
    app.run(host='localhost', port=5000)