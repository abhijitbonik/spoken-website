# currently the code in this file is not in use

import json
from django.conf import settings
import time 
import re
from geoip2.errors import AddressNotFoundError
import reverse_geocoder as rg 
import reverse_geocode

# redis, mongo, geoip2 clients
from spoken import REDIS_CLIENT, MONGO_CLIENT, GEOIP2_CLIENT


REGION_CODE_TO_REGION = {
    "AP": "Andhra Pradesh",
    "AR": "Arunachal Pradesh",
    "AS": "Assam",
    "BR": "Bihar",
    "CT": "Chhattisgarh",
    "GA": "Goa",
    "GJ": "Gujarat",
    "HR": "Haryana",
    "HP": "Himachal Pradesh",
    "JK": "Jammu and Kashmir",
    "JH": "Jharkhand",
    "KA": "Karnataka",
    "KL": "Kerala",
    "MP": "Madhya Pradesh",
    "MH": "Maharashtra",
    "MN": "Manipur",
    "ML": "Meghalaya",
    "MZ": "Mizoram",
    "NL": "Nagaland",
    "OR": "Odisha",
    "PB": "Punjab",
    "RJ": "Rajasthan",
    "SK": "Sikkim",
    "TN": "Tamil Nadu",
    "TG": "Telangana",
    "TR": "Tripura",
    "UP": "Uttar Pradesh",
    "UT": "Uttarakhand",
    "WB": "West Bengal",
    "AN": "Andaman and Nicobar Islands",
    "CH": "Chandigarh",
    "DD": "Dadra and Nagar Haveli and Daman and Diu",
    "LA": "Ladakh",
    "LD": "Lakshadweep",
    "DL": "Delhi",
    "PY": "Puducherry",
}

"""
Function called from the middleware for extracting Geolocation info,
and pushing the log to a redis queue.
Currently API-based version of the function is in use.
"""
def enqueue_log(data):

    try:
        # if the IPv4 or IPv6 address is not a properly formatted IPv4, reject it
        if not re.match(r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$', data["ip_address"]):
            if not re.match(r'^(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))$', data['ip_address']):
                return
        
        # extract Geolocation info
        try:
            location = GEOIP2_CLIENT.city(data['ip_address'])
            data["latitude"] = location["latitude"]
            data["longitude"] = location["longitude"]
            data["country"] = location["country_name"]
            data["city"] = location["city"]
            data['region_code'] = location["region"]
            data["region"] = REGION_CODE_TO_REGION.get(data["region_code"])
        except:  # check https://pypi.org/project/geoip2/ for the exceptions thrown by GeoIP2
            data["latitude"] = None
            data["longitude"] = None
            data["country"] = "Unknown"
            data["city"] = "Unknown"
            data['region_code'] = "Unknown"
            data["region"] = "Unknown"

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
