import json
from django.conf import settings
import uuid
import asyncio
import time
import redis

redis_client = redis.Redis(
    host='localhost',
    port=6379
)

def dump_json_logs(data):

    # enqueue job in the redis queue named 'tasks'
    try:
        redis_client.lpush('tasks', json.dumps(data))
        # print ('\n\nLength of tasks queue: ' + str(redis_client.llen('tasks')))
    except Exception as e:
        print (e)

    
