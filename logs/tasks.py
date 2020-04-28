# Create your Celery tasks here
from __future__ import absolute_import, unicode_literals

from celery import shared_task

# using bind=True on the shared_task decorator to turn the below function
# into a method of Task class. This lets us use self.retry for retrying
# failed tasks
@shared_task(bind=True)
def dump_json_logs(self, data):

    from django.contrib.gis.geoip2 import GeoIP2
    from geoip2.errors import AddressNotFoundError

    try:

        # first, asynchronous call to GeoIP2 database
        g = GeoIP2()

        # todo: refine exception handling
        try:
            location = g.city(data["ip_address"])  
            data["country"] = location["country_name"]
            data["city"] = location["city"]
        except AddressNotFoundError:
            data["country"] = "Unknown"
            data["city"] = "Unknown"

        # next, saving in Mongo
        # todo
        pass

    except Exception as exc:  # catching a generic exception

        # sending the task back into the queue with exponential
        # backoff
        self.retry(exc=exc, countdown=2 ** self.request.retries)
