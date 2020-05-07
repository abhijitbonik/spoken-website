# currently this code is not in use

import redis
import json
from pymongo import MongoClient

# configurations for redis
r = redis.Redis(
    host='localhost',
    port=6379
)

# create and configure the pymongo client
client = MongoClient()
db = client.log_storage
log_collection = db.log_collection

while True:

    # Wait until there's an element in the 'tasks' queue
    key, data = r.brpop('tasks')

    # Extract json data into dict
    my_json = data.decode('utf8')
    data = json.loads(my_json)

    # store in MongoDB
    log_id = log_collection.insert_one(data).inserted_id
    print (log_id)