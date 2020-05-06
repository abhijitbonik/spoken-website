# Create your Celery tasks here
from __future__ import absolute_import, unicode_literals

from celery import shared_task
from django.contrib.gis.geoip2 import GeoIP2
from geoip2.errors import AddressNotFoundError
from logs.models import WebsiteLogs
from pymongo import MongoClient
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
                                                     visited_by=data['visited_by'], ip_address=data['ip_address'], country=data['country'], state_code=data['state_code'],
                                                     city=data['city'], unique_visit=data['unique_visit'], datetime=data['datetime'])
        except Exception as e:
            with open("logs/mongo_errors_log.txt", "a") as f:
                f.write(str(e) + "\n")

        # self.retry(countdown=2, exc=e, max_retries=2) 

    except Exception as exc:  # catching a generic exception

        # sending the task back into the queue with exponential
        # backoff. If the task fails more than max_retries + 1 times,
        # an error is display in the celery worker.
        self.retry(exc=exc, countdown=2 ** self.request.retries)

# create and configure the pymongo client
client = MongoClient()
db = client.logs
logs_tutorialprogresslogs = db.logs_tutorialprogresslogs

@shared_task(bind=True)
def update_tutorial_progress(self, data):

    field = 'fosses.' + data['foss'] + '.' + data['tutorial']

    curr_time_field = field + '.curr_time'
    time_field = field + '.visit' + str (data['visit_count']) + '.minute-' + str(data['curr_time'])
    completed_field = field + '.completed'
    visit_count_field = field + '.visit_count'
    foss_language_field = 'fosses.' + data['foss'] + '.foss_lang'

    try:
        # mark as complete if current timestamp >= 80% of total length of tutorial
        # TODO: reduce redundancy
        if data['curr_time'] >= 0.8 * data['total_time']:

            logs_tutorialprogresslogs.find_one_and_update(
                { "username" : data['username'] }, 
                { "$set" : { foss_language_field: data['foss_lang'], curr_time_field: data['curr_time'], visit_count_field: data['visit_count'], completed_field: True } },
                upsert=True
            )

            logs_tutorialprogresslogs.find_one_and_update(
                { "username" : data['username'] },
                { "$push" : { time_field : data["datetime"] } },
                upsert=True
            )

            return

        # if curr_time is not yet 80% of total, OR
        # if it was marked as complete earlier, 

        logs_tutorialprogresslogs.find_one_and_update(
            { "username" : data['username'] }, 
            { "$set" : { foss_language_field: data['foss_lang'], curr_time_field: data['curr_time'], visit_count_field: data['visit_count'] } },
            upsert=True
        )
            
        logs_tutorialprogresslogs.find_one_and_update(
            { "username" : data['username'] }, 
            { "$push" : { time_field : data["datetime"] } },
            upsert=True
        )
        
        
    except Exception as e:
        with open("logs/tutorial_errors_log.txt", "a") as f:
            f.write(str(e) + "\n")
