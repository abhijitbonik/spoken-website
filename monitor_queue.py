
import redis
import json
import datetime
import os
import sys

import time  # for calculating time taken

from django.conf import settings
from django.apps import apps
import django

from celery import Celery

from logs.tasks import dump_json_logs

# importing and configuring the spoken settings.py file
sys.path.append("/home/krithik/Desktop/Git/spoken-website/")  # path to the parent dir of DjangoTastypie
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spoken.settings')
django.setup()

# redis and mongo clients
from spoken import REDIS_CLIENT, MONGO_CLIENT 

# configurations for pymongo
db = MONGO_CLIENT.logs
website_logs = db.website_logs

"""
Continuosly monitor the redis 'tasks' queue length.
if reaches >= 10000 items, pop the leftmost 10000 items
and save them in MongoDB. (the items at the left of the
queue are the ones that have been in the queue the longest,
since the queue is a FIFO structure).
"""
while (True):

    if REDIS_CLIENT.llen('tasks') >= 10000:
        
        try:

            logs = REDIS_CLIENT.lrange('tasks', 0, 9999)

            # trim the queue to remove the leftmost 10000 logs
            # TODO: check if there's any opportunity for data loss, i.e.
            # if it's possible for the queue size to increase between when the function 
            # ltrim() is called, and when the queue is actually trimmed. The newest logs
            # may be lost in this case.
            REDIS_CLIENT.ltrim('tasks', start=10000, end=REDIS_CLIENT.llen('tasks'))

            for i in range(len(logs)):

                # Extract json data into dict
                my_json = logs[i].decode('utf8')
                logs[i] = json.loads(my_json)
                # print (logs[i])


            t0 = time.clock()

            if settings.SAVE_LOGS_WITH_CELERY:

                dump_json_logs.delay(logs)

            else:
        
                # insert into MongoDB
                # the ordered=False option ensures that all the logs are attempted for insert,
                # even if one of the intermediate logs fails the insertion.
                website_logs.insert_many([logs[i] for i in range(len(logs))], ordered=False)

            t1 = time.clock() - t0

            print("Time elapsed: ", t1) # CPU seconds elapsed (floating point)

        except Exception as e:
            print (e)
