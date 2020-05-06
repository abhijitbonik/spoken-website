from django.shortcuts import render
from django.http import HttpResponse
from .tasks import update_tutorial_progress
import datetime
import math

from django.views.decorators.csrf import csrf_exempt
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