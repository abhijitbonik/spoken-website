from .urls_to_events import EVENT_NAME_DICT
import re
from .utils import enqueue_log
import datetime
import asyncio
import requests

# def getLoop():

#     loop = None
    
#     try:
#         loop = asyncio.get_event_loop()
#     except RuntimeError:
#         loop = asyncio.new_event_loop()
#         asyncio.set_event_loop(loop)
    
#     return loop


class Logs:

    def __init__(self, get_response):
        self.LOG_CLASS = "MIDDLEWARE"
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            for key in EVENT_NAME_DICT.keys():
                if re.match(key, request.META['PATH_INFO']):
                    data = {}
                    data['path_info'] = request.META['PATH_INFO']
                    data['browser_info'] = request.META['HTTP_USER_AGENT']
                    data['event_name'] = EVENT_NAME_DICT[key]['name']
                    data['visited_by'] = request.user.username if request.user.is_authenticated else 'anonymous'
                    data['ip_address'] = request.META['REMOTE_ADDR']
                    data['method'] = request.method
                    data['datetime'] = str(datetime.datetime.now())
                    data['view_args'] = view_args
                    data['view_kwargs'] = view_kwargs
                    data['request'] = request.body
                    data['referer'] = request.META.get('HTTP_REFERER', '(No referring link)')

                    # device details
                    data['browser_family'] = request.user_agent.browser.family
                    data['browser_version'] = request.user_agent.browser.version_string

                    data['os_family'] = request.user_agent.os.family
                    data['os_version'] = request.user_agent.os.version_string

                    data['device_family'] = request.user_agent.device.family
                    data['device_type'] = 'Unknown'

                    if request.user_agent.is_mobile:
                        data['device_type'] = 'Mobile'
                    
                    if request.user_agent.is_tablet:
                        data['device_type'] = 'Tablet'

                    if request.user_agent.is_pc:
                        data['device_type'] = 'PC'

                    if request.user_agent.is_mobile:
                        data['device_type'] = 'Mobile'

                    if request.user_agent.is_bot:
                        data['device_type'] = 'Search Engine Crawler/Spider'

                    if 'has_visited' in request.session:
                        data['first_time_visit'] = False
                    else:
                        data['first_time_visit'] = True
                        request.session['has_visited'] = True
                    
                    request.session.set_expiry(15552000)  # 6 months, in seconds

                    if request.method == "POST":

                        # Note that request.POST can contain multiple items for each key. 
                        # If you are expecting multiple items for each key, you can use lists, 
                        # which returns all values as a list.
                        for key, values in request.POST.lists():

                            if key != 'csrfmiddlewaretoken' and key != 'password':
                                
                                if len(values) == 1:
                                    data[key] = values[0]

                                else:
                                    data[key] = values

                    try:
                        # set a very small timeout for the HTTP request, to simulate asynchronous behaviour.
                        requests.post("http://192.168.100.6:8001/logs_api/save_middleware_log/", data=data, timeout=0.0000000001)
                    except requests.exceptions.ReadTimeout: 
                        pass

                    # loop = getLoop()
                    # loop.run_in_executor(None, enqueue_log, data)

                    break
        
        except Exception as e:
            print("Log Exception " + str(e))
        
        return None