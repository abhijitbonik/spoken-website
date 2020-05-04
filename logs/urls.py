from django.conf.urls import url
from logs.views import *

app_name = 'logs'

urlpatterns = [
    url(r'^save_tutorial_progress/$', save_tutorial_progress, name='save_tutorial_progress'),
]