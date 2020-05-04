from django.shortcuts import render
from django.http import HttpResponse
from logs.models import TutorialProgressLogs

# Create your views here.

# TODO: don't let users make their own post requests to this view
def save_tutorial_progress (request):

    if request.method != "POST":
        return HttpResponse("You are not allowed to make that request to this page.")

    username = request.POST.get("name")
    foss = request.POST.get("foss")
    tutorial = request.POST.get("tutorial")
    timestamp = request.POST.get("timestamp")

    curr_log = None

    try:
        curr_log = TutorialProgressLogs.objects.using('logs').get (username=username)
    except TutorialProgressLogs.DoesNotExist:
        curr_log = TutorialProgressLogs.objects.using('logs').create (
            username=username,
            fosses={
                
            }
        )
    
    curr_foss_log = curr_log.filter(fosses_name={'foss_name': foss})
    # curr_tutorial_logs = 

    if curr_logs['fosses'] is None:
        pass


    return HttpResponse(status=200)