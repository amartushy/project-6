"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""

import flask
from flask import request
import arrow  # Replacement for datetime, based on moment.js
import acp_times
import config

import logging
from flask_pymongo import PyMongo

###
# Globals
###
app = flask.Flask(__name__)
CONFIG = config.configuration()
app.config["MONGO_URI"] = "mongodb://mongo:27017/db"
mongo = PyMongo(app)


###
# Pages
###


@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    return flask.render_template('404.html'), 404



#Project 5 Event Handlers
@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    
    #Data verification checks
    if not isinstance(data, list):
        app.logger.error("Received data is not a list")
        return flask.jsonify({"error": "Invalid data format"}), 400
    if mongo.db is None:
        return flask.jsonify({"error": "Database not initialized"}), 500
    try:
        
        # Clear existing data in the collection
        mongo.db.control_times.delete_many({})

        # Insert new data
        mongo.db.control_times.insert_many(data)
            
    except Exception as e:
        app.logger.error(f"Error inserting data: {e}")
        return flask.jsonify({"error": str(e)}), 500
    return flask.jsonify({"message": "Data submitted successfully"}), 200



@app.route('/display', methods=['GET'])
def display():
    try:
        data_cursor = mongo.db.control_times.find({}, {'_id': 0})
        data_list = list(data_cursor)
        return flask.jsonify(data_list)

    except Exception as e:
        app.logger.error(f"Error retrieving data: {e}")
        return flask.jsonify({"error": str(e)}), 500

    
    
    

###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############

@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects URL-encoded arguments for the number of kilometers ('km'),
    the brevet distance ('brevet_dist'), and the brevet start time ('start_time').
    """
    app.logger.debug("JSON request received")
    km = request.args.get('km', type=float)
    brevet_dist = request.args.get('brevet_dist', type=float)
    start_time = request.args.get('start_time', type=str)
    app.logger.debug("km={}".format(km))
    app.logger.debug("brevet_dist={}".format(brevet_dist))
    app.logger.debug("start_time={}".format(start_time))
    app.logger.debug("request.args: {}".format(request.args))

    # Parse the start time using arrow
    start_arrow = arrow.get(start_time, 'YYYY-MM-DDTHH:mm')

    # Calculate open and close times using acp_times module
    open_time = acp_times.open_time(km, brevet_dist, start_arrow).format('YYYY-MM-DDTHH:mm')
    close_time = acp_times.close_time(km, brevet_dist, start_arrow).format('YYYY-MM-DDTHH:mm')
    result = {"open": open_time, "close": close_time}
    return flask.jsonify(result=result)



#############

app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")
