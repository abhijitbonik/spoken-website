# Create your Celery tasks here
from __future__ import absolute_import, unicode_literals

from celery import shared_task
from logs.models import WebsiteLogs
from pymongo import MongoClient
import datetime

# mongo client
from spoken import MONGO_CLIENT

# configurations for pymongo
db = MONGO_CLIENT.logs
website_logs = db.website_logs

# using bind=True on the shared_task decorator to turn the below function
# into a method of Task class. This lets us use self.retry for retrying
# failed tasks
@shared_task(bind=True)
def dump_json_logs(self, logs):

    # store in MongoDB
    try:

        # convert datetime from str to datetime object
        for i in range (len(logs)):
            logs[i]['datetime'] = datetime.datetime.strptime(logs[i]['datetime'], '%Y-%m-%d %H:%M:%S.%f')
        
        website_logs.insert_many([logs[i] for i in range(len(logs))])

    except Exception as exc:  # catching a generic exception

        # sending the task back into the queue with exponential
        # backoff. If the task fails more than max_retries + 1 times,
        # an error is display in the celery worker.
        self.retry(exc=exc, countdown=2 ** self.request.retries)

db = MONGO_CLIENT.logs
tutorial_progress_logs = db.tutorial_progress_logs

@shared_task(bind=True)
def update_tutorial_progress(self, data):

    field = 'fosses.' + data['foss_id'] + '.' + data['language_id'] + '.' + data['tutorial_id']

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
