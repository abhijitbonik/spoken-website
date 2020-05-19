
import json
from django.conf import settings
import uuid
import asyncio
import time
import redis
import re
from django.contrib.gis.geoip2 import GeoIP2
from geoip2.errors import AddressNotFoundError

# mongo client
from spoken import REDIS_CLIENT, MONGO_CLIENT


# initializing the GeoIP2 client
g = GeoIP2()

def enqueue_log(data):

    try:

        # if the IP address is not a properly formatted IPv4, reject it
        # otherwise it can crash the worker due to GeoIP throwing an error
        if not re.match(r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$', data["ip_address"]):
            return

        try:
            location = g.city(data['ip_address'])
            data["latitude"] = location["latitude"]
            data["longitude"] = location["longitude"]
            data["country"] = location["country_name"]
            data["city"] = location["city"]
            data['state_code'] = location["region"]
        except:
            data["latitude"] = None
            data["longitude"] = None
            data["country"] = "Unknown"
            data["city"] = "Unknown"
            data['state_code'] = "Unknown"

        # sometimes the Geolocation may not return some of the fields
        if not data["country"]:
            data["country"] = "Unknown"

        if not data["state_code"]:
            data["state_code"] = "Unknown"

        if not data["city"]:
            data["city"] = "Unknown"

        # enqueue job in the redis queue named 'tasks2'
        REDIS_CLIENT.rpush('tasks', json.dumps(data))

    except Exception as e:
        with open ("enqueue_logs_errors.txt", "a") as f:
            f.write (str(e))


db = MONGO_CLIENT.logs
tutorial_progress_logs = db.tutorial_progress_logs

def update_tutorial_progress(data):

    field = 'fosses.' + str(data['foss_id']) + '.' + str(data['language_id']) + '.' + str(data['tutorial_id'])

    curr_time_field = field + '.curr_time'
    time_field = field + '.visits.' + str (data['language_visit_count']) + '.minute-' + str(data['curr_time'])
    completed_field = field + '.completed'

    try:
        # mark as complete if current timestamp >= 80% of total length of tutorial
        if data['curr_time'] >= 0.8 * data['total_time']:

            tutorial_progress_logs.find_one_and_update(
                { "username" : data['username'] }, 
                { "$set" : { curr_time_field: data['curr_time'], completed_field: True } },
                upsert=True
            )

            tutorial_progress_logs.find_one_and_update(
                { "username" : data['username'] },
                { "$push" : { time_field : data["datetime"] } },
                upsert=True
            )

            return

        # if curr_time is not yet 80% of total

        tutorial_progress_logs.find_one_and_update(
            { "username" : data['username'] }, 
            { "$set" : { curr_time_field: data['curr_time'] } },
            upsert=True
        )
            
        tutorial_progress_logs.find_one_and_update(
            { "username" : data['username'] }, 
            { "$push" : { time_field : data["datetime"] } },
            upsert=True
        )
        
        
    except Exception as e:
        with open("logs/tutorial_errors_log.txt", "a") as f:
            f.write(str(e) + "\n")
