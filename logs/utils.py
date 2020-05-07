# currently this code does not serve any purpose

import json
from django.conf import settings
import uuid
import asyncio
import time
import redis
import re

# configurations for redis
redis_client = redis.Redis(
    host = 'localhost',
    port = 6379
)

def dump_json_logs(data):

    
    try:
        # enqueue job in the redis queue named 'tasks2'

        redis_client.lpush('tasks2', json.dumps(data))

    except Exception as e:
        with open ("file.txt", "a") as f:
            f.write (str(e))
