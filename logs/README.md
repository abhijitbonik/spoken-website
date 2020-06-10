## Instructions to setup the middleware-based event logging system

<<<<<<< Updated upstream
- Reinstall requirements

- In the spoken [settings.py](../spoken/settings.py) file, change the LOGS_API_URL value as required, to the URL of the logs api in spoken-analytics-system.  

- Ensure that the [spoken-analytics-system](https://github.com/Spoken-tutorial/Spoken-Analytics-System/) Django server (which contains the Logs API), is running at the URL value assigned to LOGS_API_URL. Also ensure that the other setup mentioned in the analytics system repo (running the *monitor_queue.py* file, running Celery, etc.) is done. 
  
- Report for the Spoken Tutorial Event Logging system can be found [here](https://docs.google.com/document/d/1YXwQmeMuMrX0YKncGss35xBPszmqwgO2zt37Oj0-0Vk/)
- Check the [README](/home/krithik/Desktop/Git/spoken-website/logs/README.md) of the Logs API of the Spoken-Analytics-System repo for more details.
- Link to presentation video: https://drive.google.com/file/d/1MxgjGecnsIjRe7RS8GWwE61BneNbGoqU/view?usp=sharing
=======
- After doing the normal steps to setup the spoken-website locally,

```pip install -r requirements-new.txt```

- In the spoken [settings.py](../spoken/settings.py) file, change the LOGS_API_URL value as required, to the URL of the logs api in spoken-analytics-system.  

- Ensure that the MongoDB is running. In the spoken [\_\_init\_\_.py](../spoken/__init__.py) file, change the parameters for the MongoClient, as required (currently, no parameters are being sent). Check [here](https://api.mongodb.com/python/current/api/pymongo/mongo_client.html) for the documentation of MongoClient.  

- Whenever a new URL is created in the Spoken website, add it to the [urls_to_events.py](urls_to_events.py) file.  

- Ensure that the [spoken-analytics-system](https://github.com/Spoken-tutorial/Spoken-Analytics-System/) Django server (which contains the Logs API), is running at the URL value assigned to LOGS_API_URL. Also ensure that the other setup mentioned in the analytics system repo (running the *monitor_queue.py* file, running Celery, etc.) is done. 
  
- Report for the Spoken Tutorial Event Logging system can be found [here](https://www.notion.so/krithik/Fellowship-Report-509f52a54ee94a2e9b650d41f6c3235f) (Work in Progress)

In the JS implementation, logs app only used for Context processor.
>>>>>>> Stashed changes
