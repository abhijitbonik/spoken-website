
import re
import datetime
import requests
import json

from .urls_to_events import EVENT_NAME_DICT
from django.conf import settings

class Logs:

    def __init__(self, get_response):
        self.LOG_CLASS = "MIDDLEWARE"
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):

        # get event name and log data for given URL

        try:

            for key in EVENT_NAME_DICT.keys():

                if re.match(key, request.META['PATH_INFO']):

                    data = {}
                    data['path_info'] = request.META['PATH_INFO']
                    data['event_name'] = EVENT_NAME_DICT[key]['name']
                    data['visited_by'] = request.user.username if request.user.is_authenticated else 'AnonymousUser'
                    data['ip_address'] = request.META['REMOTE_ADDR']
                    data['method'] = request.method
                    data['datetime'] = str(datetime.datetime.utcnow())
                    data['view_args'] = view_args if view_args else []
                    data['view_kwargs'] = view_kwargs if view_kwargs else {}
                    data['referer'] = request.META.get('HTTP_REFERER', '(No referring link)')
                    data['page_title'] = ""

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

                    elif request.user_agent.is_pc:
                        data['device_type'] = 'PC'

                    elif request.user_agent.is_mobile:
                        data['device_type'] = 'Mobile'

                    elif request.user_agent.is_bot:
                        data['device_type'] = 'Search Engine Crawler/Spider'

                    if 'has_visited' in request.session:
                        data['first_time_visit'] = "false"

                    else:
                        data['first_time_visit'] = "true"
                        request.session['has_visited'] = True
                    
                    request.session.set_expiry(15552000)  # 6 months, in seconds

                    if request.method == "POST":

                        data['post_data'] = {}

                        # Note that request.POST can contain multiple items for each key. 
                        for key, values in request.POST.lists():

                            # Avoid storing sensitive data.
                            if key != 'csrfmiddlewaretoken' and key != 'password':
                                
                                if len(values) == 1:
                                    data['post_data'][key] = values[0]

                                else:
                                    data['post_data'][key] = values
                        
                        data['post_data'] = json.dumps(data['post_data'])

                    try:

                        save_middleware_log_url = settings.ANALYTICS_SYSTEM_URL + 'logs_api/save_middleware_log/'
                        
                        # set a very small timeout for the HTTP request, to simulate asynchronous behaviour.
                        requests.post(save_middleware_log_url, data=data, timeout=0.0000000001)
                    
                    except requests.exceptions.ReadTimeout: 
                        pass

                    break
        
        except Exception as e:
            print("Log Exception " + str(e))
        
        return None