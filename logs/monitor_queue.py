import redis
import json
from pymongo import MongoClient

# Configure our redis client 
r = redis.Redis(
    host='localhost',
    port=6379
)

# Create and configure our pymongo client

client = MongoClient()  # connect on the default host and port
db = client.log_storage  # database
log_collection = db.log_collection  # collection of database

while True:

    # Wait until there's an element in the 'tasks' queue
    key, data = r.brpop('tasks')

    # Extract json data into dict
    my_json = data.decode('utf8')
    data = json.loads(my_json)

    # store in MongoDB
    log_id = log_collection.insert_one(data).inserted_id
    print (log_id)