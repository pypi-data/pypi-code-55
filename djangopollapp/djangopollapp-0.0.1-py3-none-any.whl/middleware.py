from .models import ClientsID


# Generates a unique id or checks its presence in cookies
class PollMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_anonymous:
            if 'client_id' not in request.COOKIES:
                client_id = ClientsID.objects.create()
                response.set_cookie('client_id', client_id.unique_id)
                return response
            else:
                try:
                    ClientsID.objects.get(unique_id=request.COOKIES.get('client_id'))
                    return response
                except ClientsID.DoesNotExist:
                    client_id = ClientsID.objects.create()
                    response.set_cookie('client_id', client_id.unique_id)
                    return response
        else:
            return response