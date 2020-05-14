# Create your Celery tasks here
from __future__ import absolute_import, unicode_literals

from celery import shared_task
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
