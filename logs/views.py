from django.shortcuts import render
from django.http import HttpResponse
from .tasks import update_tutorial_progress
import datetime
import math

from django.views.decorators.csrf import csrf_exempt

# mongo client
from spoken import MONGO_CLIENT

# Create your views here.

# TODO: don't let users make their own post requests to this view. Remove CSRF exempt
@csrf_exempt
def save_tutorial_progress (request):

    if request.method != "POST":
        return HttpResponse("You are not allowed to make that request to this page.")

    data = {}
    data['username'] = request.POST.get("username")
    data['foss'] = request.POST.get("foss")
    data['foss_lang'] = request.POST.get("foss_lang")
    data['tutorial'] = request.POST.get("tutorial")
    data['curr_time'] = int (request.POST.get("curr_time"))
    data['total_time'] = int (request.POST.get("total_time"))

    # sometimes, on the first video play,
    # this duration is returned as 0 by video.js
    if (data['total_time'] == 0):
        data['total_time'] = math.inf

    data['visit_count'] = int (request.POST.get("visit_count"))
    data['datetime'] = datetime.datetime.fromtimestamp(int (request.POST.get("timestamp"))/1000)

    update_tutorial_progress.delay (data)

    return HttpResponse(status=200)

# TODO: don't let users make their own post requests to this view. Remove CSRF exempt
@csrf_exempt
def change_completion (request):

    if request.method != "POST":
        return HttpResponse("You are not allowed to make that request to this page.")

    # configurations for pymongo
    db = MONGO_CLIENT.logs
    tutorial_progress_logs = db.tutorial_progress_logs

    # store in MongoDB
    try:
        
        completed = False
        if request.POST.get("completed") == "true":
            completed = True

        # TODO: don't allow dots in the FOSS names and tutorial names
        completed_field = 'fosses.' + request.POST.get('foss') + '.' + request.POST.get('tutorial') + '.completed'
        res = tutorial_progress_logs.find_one_and_update(
                { "username" : request.POST.get('username') }, 
                { "$set" : { completed_field: completed } },
                upsert=True
        )

        print (res)

        return HttpResponse(status=200)

    except Exception as e:
        print (str(e))
        return HttpResponse(status=500)


# TODO: don't let users make their own post requests to this view. Remove CSRF exempt
@csrf_exempt
def check_completion (request):

    if request.method != "POST":
        return HttpResponse("You are not allowed to make that request to this page.")

    # configurations for pymongo
    db = MONGO_CLIENT.logs
    tutorial_progress_logs = db.tutorial_progress_logs

    try:

        res = tutorial_progress_logs.find_one(
            { "username" : request.POST.get('username') }
        )

        if res['fosses'][request.POST.get('foss')][request.POST.get('tutorial')]['completed']:
            return HttpResponse(status=200)

        return HttpResponse(status=500)

    except Exception as e:
        print (str(e))
        return HttpResponse(status=500)