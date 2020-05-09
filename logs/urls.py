from django.conf.urls import url
from logs.views import *

app_name = 'logs'

urlpatterns = [
    url(r'^save_tutorial_progress/$', save_tutorial_progress, name='save_tutorial_progress'),
    url(r'^change_completion/$', change_completion, name='change_completion'),
    url(r'^check_completion/$', check_completion, name='check_completion'),
]