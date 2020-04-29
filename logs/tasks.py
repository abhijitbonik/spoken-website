# Create your Celery tasks here
from __future__ import absolute_import, unicode_literals

from celery import shared_task
from pymongo import MongoClient
import json
import datetime
from django.contrib.gis.geoip2 import GeoIP2
from geoip2.errors import AddressNotFoundError

# using bind=True on the shared_task decorator to turn the below function
# into a method of Task class. This lets us use self.retry for retrying
# failed tasks
@shared_task(bind=True)
def dump_json_logs(self, data):

    try:

        # first, we make a call to the GeoIP2 database
        g = GeoIP2()

        # todo: refine exception handling
        try:
            location = g.city(data["ip_address"])
            data["country"] = location["country_name"]
            data["city"] = location["city"]
            data['state_code'] = location["region"]
        except AddressNotFoundError:
            data["country"] = "Unknown"
            data["city"] = "Unknown"
            data['state_code'] = "Unknown"

        data['datetime'] = datetime.datetime.strptime(data['datetime'], '%Y-%m-%dT%H:%M:%S.%f')

        # next, saving in Mongo

        # create and configure the pymongo client
        client = MongoClient()
        db = client.logs
        website_logs = db.website_logs

        data_without__id = {}
        for key, value in data.items():
            if key != "_id":
                data_without__id[key] = value

        # store in MongoDB
        try:
            website_logs.insert_one(data_without__id)
        except Exception as e:
            with open("mongo_errors_log.txt", "a") as f:
                f.write(str(e) + "\n")

    except Exception as exc:  # catching a generic exception

        # sending the task back into the queue with exponential
        # backoff. If the task fails more than max_retries + 1 times,
        # an error is display in the celery worker.
        self.retry(exc=exc, countdown=2 ** self.request.retries)
