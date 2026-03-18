import pymongo
import os
from flask import Blueprint, render_template, request
from dotenv import load_dotenv
load_dotenv()


search = Blueprint('search', __name__, template_folder='templates')

@search.route('/')
def home():
    results = []
    
    if 'search' in request.args:
        client = pymongo.MongoClient(os.environ.get('MONGODB_URI'))

        db = client.Crawlex

        search_results = db.search_results.find(
            {'$text': {'$search': request.args.get('search')}})
        
        results = list(search_results)
        client.close()

    return render_template('search.html', results=results)