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
    # 'DATABASES': {
    #     'default': {
    #     'ENGINE': 'djongo',
    #     'NAME': 'logs',
    #     'ENFORCE_SCHEMA': True,
    #     # 'HOST': 'localhost',
    #     # 'PORT': port_number,
    #     # 'USER': 'db-username',
    #     # 'PASSWORD': 'password',
    #     # 'AUTH_SOURCE': 'db-name',
    #     # 'AUTH_MECHANISM': 'SCRAM-SHA-1'
    #     }
    # },
    # 'CELERY_BROKER_URL': 'redis://localhost:6379/2',
    # 'CELERY_RESULT_BACKEND': 'redis://localhost:6379/3',
    # 'CELERY_ACCEPT_CONTENT': ['application/json'],
    # 'CELERY_RESULT_SERIALIZER': 'json',
    # 'CELERY_TASK_SERIALIZER': 'json'
}

settings.configure(**conf)
apps.populate(settings.INSTALLED_APPS)

from logs.models import WebsiteLogs

# configurations for redis
r = redis.Redis(
    host='localhost',
    port=6379
)

# create and configure the pymongo client
client = MongoClient()
db = client.log_storage
logs_websitelogs = db.logs_websitelogs


while (True):

    if r.llen('tasks2') >= 1000:

        try:

            logs = r.lrange('tasks2', 0, 999)
            # r.ltrim('tasks2', start=1000)

            for i in range(len(logs)):
                r.lpop('tasks2')
                print (i)
                # Extract json data into dict
                my_json = logs[i].decode('utf8')
                logs[i] = json.loads(my_json)
                # print (logs[i])
            
            t0 = time.clock()

            logs_websitelogs.insert_many([logs[i] for i in range(1000)])
            # objs = [
            # WebsiteLogs (path_info=data['path_info'], browser_info=data['browser_info'], method=data['method'], event_name=data['event_name'],
            #              visited_by=data['visited_by'], ip_address=data['ip_address'], country=data['country'], state_code=data['state_code'],
            #              city=data['city'], unique_visit=data['unique_visit'], datetime=datetime.datetime.strptime(data['datetime'], '%Y-%m-%d %H:%M:%S.%f')
            #     )
            #     for data in logs
            # ]
        
            # WebsiteLogs.objects.using('default').bulk_create(objs)
            t1 = time.clock() - t0

            print("Time elapsed: ", t1) # CPU seconds elapsed (floating point)

        except Exception as e:
            print (e)
