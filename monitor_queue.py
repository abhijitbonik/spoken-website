# currently this code is not in use

import redis
import json
import datetime
from django.conf import settings
import os
from pymongo import MongoClient
from django.apps import apps

# importing the required module 
import time

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
    },
    'BROKER_URL': 'redis://localhost:6379/0',
    'RESULT_BACKEND': 'redis://localhost:6379/1',
    'ACCEPT_CONTENT': ['application/json'],
    'RESULT_SERIALIZER': 'json',
    'TASK_SERIALIZER': 'json',
    'CELERY_BROKER_URL': 'redis://localhost:6379/0',
    'CELERY_RESULT_BACKEND': 'redis://localhost:6379/1',
    'CELERY_ACCEPT_CONTENT': ['application/json'],
    'CELERY_RESULT_SERIALIZER': 'json',
    'CELERY_TASK_SERIALIZER': 'json'
}

settings.configure(**conf)
apps.populate(settings.INSTALLED_APPS)

# configurations for redis
r = redis.Redis(
    host='localhost',
    port=6379,
    db=0
)

# create and configure the pymongo client
# client = MongoClient()
# db = client.log_storage
# logs_websitelogs = db.logs_websitelogs

from celery import Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spoken.settings')
app = Celery('spoken')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

from logs.models import WebsiteLogs
from logs.tasks import dump_json_logs

while (True):

    if r.llen('tasks') >= 1000:

        try:

            logs = r.lrange('tasks', 0, 999)
            # r.ltrim('tasks', start=1000)

            for i in range(len(logs)):
                r.lpop('tasks')

                # Extract json data into dict
                my_json = logs[i].decode('utf8')
                logs[i] = json.loads(my_json)
                # print (logs[i])
            
            t0 = time.clock()

            dump_json_logs.delay(logs)

            t1 = time.clock() - t0

            print("Time elapsed: ", t1) # CPU seconds elapsed (floating point)

        except Exception as e:
            print (e)
