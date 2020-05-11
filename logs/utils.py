
import json
from django.conf import settings
import uuid
import asyncio
import time
import redis
import re
from django.contrib.gis.geoip2 import GeoIP2
from geoip2.errors import AddressNotFoundError

# configurations for redis
redis_client = redis.Redis(
    host = 'localhost',
    port = 6379,
    db = 0
)

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

        # enqueue job in the redis queue named 'tasks2'
        redis_client.rpush('tasks', json.dumps(data))

    except Exception as e:
        with open ("enqueue_logs_errors.txt", "a") as f:
            f.write (str(e))