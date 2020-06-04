## Instructions to setup the middleware-based event logging system

- After doing the normal steps to setup the spoken-website locally,

```pip install -r requirements-new.txt```

- In the spoken [settings.py](../spoken/settings.py) file, change the LOGS_API_URL value as required, to the URL of the logs api in spoken-analytics-system.  

- Ensure that the MongoDB is running. In the spoken [\_\_init\_\_.py](../spoken/__init__.py) file, change the parameters for the MongoClient, as required (currently, no parameters are being sent). Check [here](https://api.mongodb.com/python/current/api/pymongo/mongo_client.html) for the documentation of MongoClient.  

- Whenever a new URL is created in the Spoken website, add it to the [urls_to_events.py](urls_to_events.py) file.  

- Ensure that the [spoken-analytics-system](https://github.com/Spoken-tutorial/Spoken-Analytics-System/) Django server (which contains the Logs API), is running at the URL value assigned to LOGS_API_URL. Also ensure that the other setup mentioned in the analytics system repo (running the *monitor_queue.py* file, running Celery, etc.) is done. 
  
- Report for the Spoken Tutorial Event Logging system can be found [here](https://www.notion.so/krithik/Fellowship-Report-509f52a54ee94a2e9b650d41f6c3235f) (Work in Progress)