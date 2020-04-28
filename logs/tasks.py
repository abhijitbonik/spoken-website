# Create your Celery tasks here
from __future__ import absolute_import, unicode_literals

from celery import shared_task


# using bind=True on the shared_task decorator to turn the below function
# into a method of Task class. This lets us use self.retry for retrying
# failed tasks
@shared_task(bind=True, max_retries=3)
def dump_json_logs(self, data):

    try:

        # code goes here
        pass

    except Exception as exc:  # catching a generic exception

        # sending the task back into the queue with exponential
        # backoff
        self.retry(exc=exc, countdown=2 ** self.request.retries)
