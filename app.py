from flask import Flask
from routes.search import search
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')
app.register_blueprint(search)

if __name__ == '__main__':
    app.run(debug=True, threaded=True)