
def ip_address_processor(request):
    return {'user_ip_address': request.META['REMOTE_ADDR']}