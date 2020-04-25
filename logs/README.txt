Will need these two additional dependencies - 
pip install redis
pip install pymongo

Explanation:

The middleware extracts the relevant log info from the request and stores it in a dict. 
Then it calls dump_json_logs on a separate thread (hence non blocking), which adds this 
dict to a redis queue named 'tasks'. 

To consume the items from the queue, another python script (monitor_queue.py) is kept
running. The script repeatedly checks for items in the 'tasks' queue of redis, extracts 
an item if the queue is not empty and stores them in MongoDB.

This setup has been tested locally.

To speed up the consumer, we can consider using multiprocessing to run multiple consumers
parallely.
