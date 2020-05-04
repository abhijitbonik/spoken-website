# 25/04

## Additional dependencies:
pip install redis  
pip install pymongo  

## Explanation:

The middleware extracts the relevant log info from the request and stores it in a dict. 
Then it calls dump_json_logs on a separate thread (hence non blocking), which adds this 
dict to a redis queue named 'tasks'. 

To consume the items from the queue, another python script (monitor_queue.py) is kept
running. The script repeatedly checks for items in the 'tasks' queue of redis, extracts 
an item if the queue is not empty and stores them in MongoDB.

This setup has been tested locally.

# Other approaches

Tried to use asyncio 
To speed up the consumer, we can consider using multiprocessing to run multiple consumers
parallely.

# 27/04

### Additional dependencies:
pip install celery

The Django project has been setup to use a Celery task processing queue, with Redis as  
the message broker between the Django application and Celery.  

Next steps would be to possibly create a result backend, store celery logs, optimize worker  
performance, set task failure behaviour, etc.  

# 28/04

#### Running a celery instance

Ensure that the redis server is running  

> celery -A spoken worker -l INFO -f celery.logs  

-A - appname  
-l - loglevel  
-f - log file path. If no logfile is specified, stderr is used.  

- Added generic exception handling
- Ignore backend results to improve performance

#### Mongo validation design (in progress)

path pattern: "^(/(.)*)*/$" - matches /.../.../
event pattern - matches event. anything  
Todo: add bsontypes for "request_data", "view_args", "view_kwargs"  

#### Merged logs branch into my branch

#### GeoIP2

Using Geolite2 databases (free)  
Downloaded the binaries and saved in geodb/. Total size ~ 68mb  
We can extract the country, state code (more accurately, the region) and city with this.  

Todo: cron job to update the db everyweek - https://mauteam.org/mautic/mautic-admins/solved-maxmind-geolite2-database-not-updating/    

License  
The GeoLite2 end-user license agreement, which incorporates components of the Creative Commons   Attribution-ShareAlike 4.0 International License can be found here. The attribution requirement may be met by   including the following in all advertising and documentation mentioning features of or use of this database:  

This product includes GeoLite2 data created by MaxMind, available from  
<a href="https://www.maxmind.com">https://www.maxmind.com</a>.  


#### Added date & time to logs.

# 29/04

### Todo 
make the shared_task function lighter?
other mongo validations - check whether the db exists, collection exists.  
add tzinfo  
refine exception handling  
move the database files from the repository to somewhere else?  

### Ideas
do the IP geolocation only once and store it in the session   

# 30/04, 01/05

- Fixed regex matching in middleware  
- Applied validation schema to the logs_websitelogs MongoDB collection (check schema.txt for the applied schema). It does additional validations like comparing with RegEx's, etc. that the Djongo model does not do.  
- Refined error handling for GeoIP
- Updated requirements file  
- Timed the two asynchronous queries, querying geoip db is about 2 orders of magnitude faster than saving in mongo. Tried turning of schema validation, made no noticeable difference.

# 02/05

- Added unique/returning visits tracking (a visit is considered returning if the user has visited the website in the past 6 months, from the same browser)  
- Refining checking of returning visits by also checking username?

# 04/05

- Tutorial progress logs
- Attempted to create schema in Djongo






