# Create your Celery tasks here
from __future__ import absolute_import, unicode_literals

from celery import shared_task
from django.contrib.gis.geoip2 import GeoIP2
from geoip2.errors import AddressNotFoundError
from logs.models import WebsiteLogs
import re

# initializing the GeoIP2 client
g = GeoIP2()

# using bind=True on the shared_task decorator to turn the below function
# into a method of Task class. This lets us use self.retry for retrying
# failed tasks
@shared_task(bind=True)
def dump_json_logs(self, data):

    global g

    try:

        # if the IP address is not a properly formatted IPv4, reject it
        # otherwise it can crash the Celery worker due to GeoIP throwing an error
        if not re.match(r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$', data["ip_address"]):
            return

        try:
            location = g.city(data["ip_address"])
            data["country"] = location["country_name"]
            data["city"] = location["city"]
            data['state_code'] = location["region"]
        except AddressNotFoundError:
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

        # store in MongoDB
        try:
            WebsiteLogs.objects.using('logs').create(path_info=data['path_info'], browser_info=data['browser_info'], method=data['method'], event_name=data['event_name'],
                                                     visited_by=data['visited_by'], ip_address=data['ip_address'], country=data['country'], state_code=data['state_code'], city=data['city'])
        except Exception as e:
            with open("logs/mongo_errors_log.txt", "a") as f:
                f.write(str(e) + "\n")

    except Exception as exc:  # catching a generic exception

        # sending the task back into the queue with exponential
        # backoff. If the task fails more than max_retries + 1 times,
        # an error is display in the celery worker.
        self.retry(exc=exc, countdown=2 ** self.request.retries)
