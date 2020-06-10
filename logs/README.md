## Instructions to setup the middleware-based event logging system

- NOTE: Please modify static/spoken/js/base.js here and modify save_js_logs() view in analytics system, and change the placeholder region data with the system of your choice.

- Reinstall requirements

- In the spoken [settings.py](../spoken/settings.py) file, change the LOGS_API_URL value as required, to the URL of the logs api in spoken-analytics-system.  

- Ensure that the [spoken-analytics-system](https://github.com/Spoken-tutorial/Spoken-Analytics-System/) Django server (which contains the Logs API), is running at the URL value assigned to LOGS_API_URL. Also ensure that the other setup mentioned in the analytics system repo (running the *monitor_queue.py* file, running Celery, etc.) is done. 
  
- Report for the Spoken Tutorial Event Logging system can be found [here](https://docs.google.com/document/d/1YXwQmeMuMrX0YKncGss35xBPszmqwgO2zt37Oj0-0Vk/)
- Check the [README](/home/krithik/Desktop/Git/spoken-website/logs/README.md) of the Logs API of the Spoken-Analytics-System repo for more details.
- Link to presentation video: https://drive.google.com/file/d/1MxgjGecnsIjRe7RS8GWwE61BneNbGoqU/view?usp=sharing
