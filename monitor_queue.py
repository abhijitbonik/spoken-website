# currently this code is not in use

import redis
import json
from pymongo import MongoClient
from django.conf import settings
import uuid
import asyncio
import time
import re
import datetime
import django

import os
from django.apps import apps

conf = {
    'INSTALLED_APPS': [
        'logs'
    ],
    'DATABASES': {
        'default': {
        'ENGINE': 'djongo',
        'NAME': 'logs',
        'ENFORCE_SCHEMA': True,
        # 'HOST': 'localhost',
        # 'PORT': port_number,
        # 'USER': 'db-username',
        # 'PASSWORD': 'password',
        # 'AUTH_SOURCE': 'db-name',
        # 'AUTH_MECHANISM': 'SCRAM-SHA-1'
    }
    }
}

settings.configure(**conf)
apps.populate(settings.INSTALLED_APPS)

from logs.models import WebsiteLogs

# configurations for redis
r = redis.Redis(
    host='localhost',
    port=6379
)

# create and configure the pymongo client
client = MongoClient()
db = client.log_storage
log_collection = db.log_collection


for i in range (10000):

    print ('hmm')
    try:

        # Wait until there's an element in the 'tasks' queue
        key, data = r.brpop('tasks2')
        
        # Extract json data into dict
        my_json = data.decode('utf8')
        data = json.loads(my_json)

        # if the IP address is not a properly formatted IPv4, reject it
        # otherwise it can crash the Celery worker due to GeoIP throwing an error
        if not re.match(r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$', data["ip_address"]):
            continue

        try:
            location = {'country': 'a'}
            data["country"] = location["country_name"]
            data["city"] = location["city"]
            data['state_code'] = location["region"]
        except:
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

        data["datetime"] = datetime.datetime.now()

        # store in MongoDB
        WebsiteLogs.objects.create(path_info=data['path_info'], browser_info=data['browser_info'], method=data['method'], event_name=data['event_name'],
                                                 visited_by=data['visited_by'], ip_address=data['ip_address'], country=data['country'], state_code=data['state_code'],
                                                 city=data['city'], unique_visit=data['unique_visit'], datetime=data['datetime'])
        
        print ("OK\n\n\n")
    except Exception as e:
        print (e)

print ('Done')