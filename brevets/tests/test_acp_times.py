"""
Nose tests for acp_times.py

Write your tests HERE AND ONLY HERE.
"""



from nose.tools import assert_equal
import arrow
from acp_times import open_time, close_time
import logging
logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=logging.WARNING)
log = logging.getLogger(__name__)

def test_open_100():
    start_time = arrow.get('2021-01-01T00:00:00+00:00')
    control_dist_km = 100
    brevet_dist_km = 200
    expected_open_time = start_time.shift(hours=+2, minutes=+56)
    assert_equal(open_time(control_dist_km, brevet_dist_km, start_time), expected_open_time)

def test_close_100():
    start_time = arrow.get('2021-01-01T00:00:00+00:00')
    control_dist_km = 100
    brevet_dist_km = 200
    expected_close_time = start_time.shift(hours=+6, minutes=+40)
    assert_equal(close_time(control_dist_km, brevet_dist_km, start_time), expected_close_time)

def test_open_200():
    start_time = arrow.get('2021-01-01T00:00:00+00:00')
    control_dist_km = 200
    brevet_dist_km = 200
    expected_open_time = start_time.shift(hours=+5, minutes=+53)
    assert_equal(open_time(control_dist_km, brevet_dist_km, start_time), expected_open_time)

def test_close_200():
    start_time = arrow.get('2021-01-01T00:00:00+00:00')
    control_dist_km = 200
    brevet_dist_km = 200
    expected_close_time = start_time.shift(hours=+13, minutes=+30)
    assert_equal(close_time(control_dist_km, brevet_dist_km, start_time), expected_close_time)

def test_close_60():
    start_time = arrow.get('2021-01-01T00:00:00+00:00')
    control_dist_km = 60
    brevet_dist_km = 200
    expected_close_time = start_time.shift(hours=+4)
    assert_equal(close_time(control_dist_km, brevet_dist_km, start_time), expected_close_time)


def test_db_insertion():
    from flask_brevets import app, mongo

    app.testing = True
    with app.app_context():
        test_data = {"miles": 100, "km": 160.934, "location": "Test Location", "open": "2021-01-01T06:00", "close": "2021-01-01T12:00"}
        mongo.db.control_times.insert_one(test_data)

        inserted_data = mongo.db.control_times.find_one({"location": "Test Location"}, {'_id': 0})
        assert_equal(inserted_data, test_data)


def test_db_retrieval():
    from flask_brevets import app, mongo

    app.testing = True
    with app.app_context():
        test_data = {"miles": 50, "km": 80.4672, "location": "Test Retrieval", "open": "2021-01-01T03:00", "close": "2021-01-01T09:00"}
        mongo.db.control_times.insert_one(test_data)

        retrieved_data = mongo.db.control_times.find_one({"location": "Test Retrieval"}, {'_id': 0})
        assert_equal(retrieved_data, test_data)
