
from django.conf import settings


def logs_processor(request):
    return {
        'user_ip_address': request.META['REMOTE_ADDR'],
        'logs_api_url': settings.LOGS_API_URL
    }
