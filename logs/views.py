from django.shortcuts import render
from django.http import HttpResponse
from .tasks import update_tutorial_progress

# Create your views here.

# TODO: don't let users make their own post requests to this view
def save_tutorial_progress (request):

    if request.method != "POST":
        return HttpResponse("You are not allowed to make that request to this page.")

    data = {}
    data['username'] = request.POST.get("name")
    data['foss'] = request.POST.get("foss")
    data['tutorial'] = request.POST.get("tutorial")
    data['curr_time'] = request.POST.get("curr_time")
    data['total_time'] = request.POST.get("total_time")

    # both, curr_time and total_time are in seconds (float)
    update_tutorial_progress.delay (data)

    return HttpResponse(status=200)