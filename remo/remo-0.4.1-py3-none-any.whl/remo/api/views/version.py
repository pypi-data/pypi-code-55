from django.http import JsonResponse
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from remo_app import __version__


class Version(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        return JsonResponse({
            'app': 'remo',
            'version': __version__
        })
