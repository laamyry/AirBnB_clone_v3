#!/usr/bin/python3
'''Status of your API'''
from flask import Flask
from models import storage
from api.v1.views import app_views as views
from os import getenv

app = Flask(__name__)
app.register_blueprint(views)


@app.teardown_appcontext
def close_storage(exception):
    """close storage"""
    storage.close()


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', "0.0.0.0")
    port = getenv('HBNB_API_PORT', "5000")
    app.run(host=host, port=port, threaded=True)
