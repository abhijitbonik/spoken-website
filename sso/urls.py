from django.conf.urls import url

from .views import metadata_view

urlpatterns = [
    url(r'metadata/', metadata_view, name='sso_metadata'),
    
]
app_name = 'sso'