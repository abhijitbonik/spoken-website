from .urls import EVENT_NAME_DICT
import requests
import json
import re
from .utils import dump_json_logs
import asyncio
from django.urls import resolve


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
            if request.META['PATH_INFO'] == '/' or re.match(r'/home/$', request.META['PATH_INFO']):
                data = {}
                data['path_info'] = request.META['PATH_INFO']
                data['browser_info'] =request.META['HTTP_USER_AGENT']
                data['request_data'] = dict(request.GET)
                data['method'] = request.method
                data['view_args'] = view_args
                data['view_kwargs'] = view_kwargs
                data['event_name'] = EVENT_NAME_DICT['home']['name']
                data['visited_by'] = request.user.username if request.user.is_authenticated else 'anonymous'
                data['ip_address'] = request.META['REMOTE_ADDR']

                loop = getLoop()
                loop.run_in_executor(None, dump_json_logs, data)
                        
            else:
                for key in EVENT_NAME_DICT.keys():
                    if re.match(key, request.META['PATH_INFO']):
                        data = {}
                        data['path_info'] = request.META['PATH_INFO']
                        data['browser_info'] = request.META['HTTP_USER_AGENT']
                        data['request_data'] = dict(request.GET)
                        data['method'] = request.method
                        data['view_args'] = view_args
                        data['view_kwargs'] = view_kwargs
                        data['event_name'] = EVENT_NAME_DICT[key]['name']
                        data['visited_by'] = request.user.username if request.user.is_authenticated else 'anonymous'
                        data['ip_address'] = request.META['REMOTE_ADDR']
                        
                        loop = getLoop()
                        loop.run_in_executor(None, dump_json_logs, data)
                        
                        break

        except Exception as e:
            print("Log Exception " + e)
        return None
