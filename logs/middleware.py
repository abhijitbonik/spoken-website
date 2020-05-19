from .urls_to_events import EVENT_NAME_DICT
import re
from .utils import enqueue_log
import datetime
import asyncio

def getLoop():

    loop = None
    
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    return loop


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
                    data['referer'] = request.META.get('HTTP_REFERER', None)

                    # device details
                    data['browser_family'] = request.user_agent.browser.family
                    data['browser_version'] = request.user_agent.browser.version_string

                    data['operating_system_family'] = request.user_agent.os.family
                    data['operating_system_version'] = request.user_agent.os.version_string

                    data['device_family'] = request.user_agent.device.family

                    if 'has_visited' in request.session:
                        data['first_time_visit'] = False
                    else:
                        data['first_time_visit'] = True
                        request.session['has_visited'] = True
                    
                    request.session.set_expiry(15552000)  # 6 months, in seconds

                    loop = getLoop()
                    loop.run_in_executor(None, enqueue_log, data)

                    break
        
        except Exception as e:
            print("Log Exception " + str(e))
        
        return None