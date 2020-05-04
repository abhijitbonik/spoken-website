from __future__ import unicode_literals

from djongo import models

# model for saving website logs
class WebsiteLogs (models.Model):

    path_info = models.CharField (max_length=200)
    browser_info = models.CharField (max_length=300)
    method = models.CharField(max_length=10)
    event_name = models.CharField (max_length=100, blank=False)
    visited_by = models.CharField (max_length=100, blank=False)
    ip_address = models.GenericIPAddressField(null=False)
    country = models.CharField (max_length=100, blank=False)
    state_code = models.CharField (max_length=10, blank=False)
    city = models.CharField (max_length=100, blank=False)
    datetime = models.DateTimeField(auto_now_add=True, auto_now=False)
    unique_visit = models.BooleanField(null=False)
    
    def __str__(self):
        return "Website Log Object"

    objects = models.DjongoManager()


# models for saving video logs

class Tutorials(models.Model):
    tutorial_id = models.CharField(max_length=100)
    progress = models.IntegerField()
    is_complete = models.BooleanField()

    class Meta:
        abstract = True


class Fosses(models.Model):
    foss_name = models.CharField(max_length=100)
    progress_of_each_tutorial = models.ArrayModelField(
        model_container=Tutorials
    )

    class Meta:
        abstract = True


class TutorialProgressLogs (models.Model):

    username = models.CharField (max_length=100, blank=False, primary_key=True)
    fosses = models.ArrayModelField(
        model_container=Fosses
    )
    
    def __str__(self):
        return "Tutorial Progress Log Object"

    objects = models.DjongoManager()
