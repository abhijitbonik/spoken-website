# currently this code is not in use

import redis
import json
import datetime
from django.conf import settings
import os
from pymongo import MongoClient
from django.apps import apps
from celery import Celery

# importing the required module 
import time

conf = {
    'CELERY_BROKER_URL': 'redis://localhost:6379/0',
    'CELERY_RESULT_BACKEND': 'redis://localhost:6379/1',
    'CELERY_ACCEPT_CONTENT': ['application/json'],
    'CELERY_RESULT_SERIALIZER': 'json',
    'CELERY_TASK_SERIALIZER': 'json',
}

settings.configure(**conf)

from logs.tasks import dump_json_logs

# configurations for redis
r = redis.Redis(
    host='localhost',
    port=6379,
    db=0
)


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spoken.settings')
app = Celery('spoken')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


while (True):

    if r.llen('tasks') >= 5:
        
        try:

            logs = r.lrange('tasks', 0, 5)
            # r.ltrim('tasks', start=1000)

            for i in range(len(logs)):
                r.lpop('tasks')

                # Extract json data into dict
                my_json = logs[i].decode('utf8')
                logs[i] = json.loads(my_json)
                # print (logs[i])
            
            print (r.llen('tasks'))

            t0 = time.clock()

            dump_json_logs.delay(logs)

            t1 = time.clock() - t0

            print("Time elapsed: ", t1) # CPU seconds elapsed (floating point)

        except Exception as e:
            print (e)
