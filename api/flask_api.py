"""
Brevets RESTful API
"""
import os
from flask import Flask
from flask_restful import Api
from mongoengine import connect


from resources.brevet import Brevet
from resources.brevets import Brevets
import logging

# Connect MongoEngine to mongodb
connect(host=f"mongodb://{os.environ['MONGODB_HOSTNAME']}:27017/brevetsdb")

# Start Flask app and Api here:
app = Flask(__name__)
api = Api(app)

# Bind resources to paths here:
# api.add_resource(...)

api.add_resource(Brevets, '/brevets')
api.add_resource(Brevet, '/brevet/<string:id>')


if __name__ == "__main__":
    # Run flask app normally
    # Read DEBUG and PORT from environment variables.
    debug = os.environ.get('DEBUG', 'False') == 'True'
    port = os.environ.get('PORT', 5000)
    app.run(debug=debug, port=int(port), host='0.0.0.0')
    # pass

