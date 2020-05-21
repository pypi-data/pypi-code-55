from django.template.response import TemplateResponse
from django.views.generic import View

from django.conf import settings
from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm

from qnc_crud import js_response

class LoginView(View):
    def get(self, request):
        return TemplateResponse(request, 'qnc_crud/login.html', dict(form=AuthenticationForm()))

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        
        if not form.is_valid() :
            return js_response.set_form_errors(form)

        auth.login(request, form.get_user())

        '''
            This works well when logging in from a public page which looks different when logged in.
            On such pages, you should include a login link with ?return=True as the query string.

            TODO - the downside to this approach, is that chrome doesn't prompt to save password
            (it seems to be waiting for the creation of a new history entry to do that)
            You can still manually save the password (from the "key" in the address bar).

            I really don't see how we can achieve this flow and still make chrome prompt to save.
            I guess it's up to the site developer if they want to use the "return" feature or not.
        '''
        if request.GET.get('return') :
            return js_response.go_back()

        '''
            Otherwise, behave similarly to django's login view.

            Rather than creating a new history entry, though, we replace the current one. 
            If the user clicks "back", they should go to wherever they were before the login page, not to the actual login page.
        '''
        redirect = request.GET.get('next') or getattr(settings, 'LOGIN_REDIRECT_URL', '/')
        return js_response.replace_location(redirect)

class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        return js_response.reload()
