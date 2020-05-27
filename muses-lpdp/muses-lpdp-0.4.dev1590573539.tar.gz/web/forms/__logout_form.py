from django.contrib.auth import logout

from web.forms import Form


class LogoutForm(Form):

    def logout(self, request):
        logout(request=request)
