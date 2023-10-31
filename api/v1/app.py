#!/usr/bin/python3
'''Status of your API'''
from os import getenv
from flask import Flask
from models import storage
from api.v1.views import app_views as views
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(views)


@app.errorhandler(400)
def not_found(error):
    message = error.description
    return message, 400

@app.errorhandler(404)
def not_found(error):
    """error"""
    return {"error": "Not found"}, 404

@app.teardown_appcontext
def close_storage(exception):
    """close storage"""
    storage.close()

if getenv("HBNB_API_HOST"):
    host = getenv("HBNB_API_HOST")
else:
    host = "0.0.0.0"

if getenv("HBNB_API_PORT"):
    port = int(getenv("HBNB_API_PORT"))
else:
    port = 5000
    
if __name__ == "__main__":
    app.run(host=host, port=port, threaded=True)
