
import json
from django.conf import settings
import time 
import re
from geoip2.errors import AddressNotFoundError
import reverse_geocoder as rg 

# redis, mongo, geoip2 clients
from spoken import REDIS_CLIENT, MONGO_CLIENT, GEOIP2_CLIENT


"""
Function called from the middleware for extracting Geolocation info,
and pushing the log to a redis queue.
"""
def enqueue_log(data):

    try:

        # if the IP address is not a properly formatted IPv4, reject it
        if not re.match(r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$', data["ip_address"]):
            return

        # extract Geolocation info
        try:
            location = GEOIP2_CLIENT.city(data['ip_address'])
            data["latitude"] = location["latitude"]
            data["longitude"] = location["longitude"]
            data["country"] = location["country_name"]
            data["city"] = location["city"]
            data['region_code'] = location["region"]
        except:
            data["latitude"] = None
            data["longitude"] = None
            data["country"] = "Unknown"
            data["city"] = "Unknown"
            data['region_code'] = "Unknown"

        data['region'] = None

        try:
            rg_result = rg.search((float (data["latitude"]), float (data["longitude"]))) 
            data["region"] = rg_result[0]['admin1']

        except Exception:
            pass

        # sometimes the Geolocation may not return some of the fields
        if not data["country"]:
            data["country"] = "Unknown"

        if not data["region_code"]:
            data["region_code"] = "Unknown"

        if not data["city"]:
            data["city"] = "Unknown"

        if not data["region"]:
            data["region"] = "Unknown"

        # enqueue job in the redis queue named 'tasks'
        REDIS_CLIENT.rpush('tasks', json.dumps(data))

    except Exception as e:
        with open("enqueue_logs_errors.txt", "a") as f:
            f.write(str(e))


# initialize the variable pointing to the tutorial_progress_logs
# MongoDB collection.
db = MONGO_CLIENT.logs
tutorial_progress_logs = db.tutorial_progress_logs


"""
Function for updating the current tutorial timestamp and associated
metadata in MongoDB. This is called from an save_tutorial_progress function in views.py
This code is currently not in use, as an API-based code is currently used instead.
"""
def update_tutorial_progress(data):

    field = 'fosses.' + str(data['foss_id']) + '.' + str(data['language_id']) + '.' + str(data['tutorial_id'])

    curr_time_field = field + '.curr_time'
    time_field = field + '.visits.' + str(data['language_visit_count']) + '.minute-' + str(data['curr_time'])
    completed_field = field + '.completed'

    try:
        # mark as complete if current timestamp >= 80% of total length of tutorial
        if data['curr_time'] >= 0.8 * data['total_time']:

            tutorial_progress_logs.find_one_and_update(
                {"username": data['username']},
                {"$set": {curr_time_field: data['curr_time'], completed_field: True}},
                upsert=True
            )

            tutorial_progress_logs.find_one_and_update(
                {"username": data['username']},
                {"$push": {time_field: data["datetime"]}},
                upsert=True
            )

            return

        # if curr_time is not yet 80% of total

        tutorial_progress_logs.find_one_and_update(
            {"username": data['username']},
            {"$set": {curr_time_field: data['curr_time']}},
            upsert=True
        )

        tutorial_progress_logs.find_one_and_update(
            {"username": data['username']},
            {"$push": {time_field: data["datetime"]}},
            upsert=True
        )

    except Exception as e:
        with open("logs/tutorial_errors_log.txt", "a") as f:
            f.write(str(e) + "\n")
