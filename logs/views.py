# currently none of these functions are in use,
# as they are being called in the other repository instead.

from django.shortcuts import render
from django.http import HttpResponse
from .utils import update_tutorial_progress
import datetime
import math

from django.views.decorators.csrf import csrf_exempt

# mongo client
from spoken import MONGO_CLIENT

# Create your views here.

"""
Function for handling the AJAX call of saving tutorial progress data. This AJAX
call is made in watch_tutorial.html. Calls update_tutorial_progress in utils.py
for the actual saving in MongoDB.
This code is currently not in use, as an API-based code is currently used instead.
TODO: don't let users make their own post requests to this view. Remove CSRF exempt
"""
@csrf_exempt
def save_tutorial_progress(request):

    if request.method != "POST":
        return HttpResponse("You are not allowed to make that request to this page.")

    data = {}
    data['username'] = request.POST.get("username")
    # data['foss'] = request.POST.get("foss")
    # data['foss_lang'] = request.POST.get("foss_lang")
    # data['tutorial'] = request.POST.get("tutorial")
    data['foss_id'] = request.POST.get("foss_id")
    data['tutorial_id'] = request.POST.get("tutorial_id")
    data['language_id'] = request.POST.get("language_id")
    data['curr_time'] = int(request.POST.get("curr_time"))
    data['total_time'] = int(request.POST.get("total_time"))

    # sometimes, on the first video play,
    # total video duration is returned as 0 by video.js
    if (data['total_time'] == 0):
        data['total_time'] = math.inf

    data['language_visit_count'] = int(request.POST.get("language_visit_count"))

    # convert JS timestamp to Python datetime
    data['datetime'] = datetime.datetime.fromtimestamp(int(request.POST.get("timestamp")) / 1000)

    update_tutorial_progress(data)

    return HttpResponse(status=200)


"""
Function for handling the AJAX call of changing tutorial completion data. This AJAX
call is made in watch_tutorial.html.
This code is currently not in use, as an API-based code is currently used instead.
TODO: don't let users make their own post requests to this view. Remove CSRF exempt
"""
@csrf_exempt
def change_completion(request):

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
        completed_field = 'fosses.' + str(request.POST.get('foss_id')) + '.' + str(
            request.POST.get('language_id')) + '.' + str(request.POST.get('tutorial_id')) + '.completed'
        tutorial_progress_logs.find_one_and_update(
            {"username": request.POST.get('username')},
            {"$set": {completed_field: completed}},
            upsert=True
        )

        return HttpResponse(status=200)

    except Exception as e:
        print(str(e))
        return HttpResponse(status=500)


"""
Function for handling the AJAX call of checking tutorial completion. This AJAX
call is made in watch_tutorial.html.
This code is currently not in use, as an API-based code is currently used instead.
TODO: don't let users make their own post requests to this view. Remove CSRF exempt
"""
@csrf_exempt
def check_completion(request):

    if request.method != "POST":
        return HttpResponse("You are not allowed to make that request to this page.")

    # configurations for pymongo
    db = MONGO_CLIENT.logs
    tutorial_progress_logs = db.tutorial_progress_logs

    try:

        user_log = tutorial_progress_logs.find_one(
            {"username": request.POST.get('username')}
        )

        # Get the exact record for given user, given FOSS, given language and given tutorial,
        # if it exists. Then check completion status. 
        user_foss = user_log['fosses'][str(request.POST.get('foss_id'))]
        user_foss_lang = user_foss[str(request.POST.get('language_id'))]
        user_tutorial = user_foss_lang[str(request.POST.get('tutorial_id'))]

        if user_tutorial['completed'] == True:
            return HttpResponse(status=200)

        return HttpResponse(status=500)

    except Exception as e:
        return HttpResponse(status=500)
