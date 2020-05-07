from .urls_to_events import EVENT_NAME_DICT
import re
from .tasks import dump_json_logs
import asyncio
import datetime
import requests
import json
import re
from .utils import dump_json_logs


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
                    # data['datetime'] = datetime.datetime.now()

                    if 'has_visited' in request.session:
                        data['unique_visit'] = False
                    else:
                        data['unique_visit'] = True
                        request.session['has_visited'] = True
                    
                    request.session.set_expiry(15552000)  # 6 months, in seconds

                    loop = getLoop()
                    loop.run_in_executor(None, dump_json_logs, data)

                    break
        
        except Exception as e:
            print("Log Exception " + e)
        
        return None