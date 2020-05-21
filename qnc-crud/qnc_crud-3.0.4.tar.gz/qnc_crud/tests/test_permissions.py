from django import http
from django.contrib.auth.models import User, Permission
from django.test import TestCase, override_settings
from django.test.client import RequestFactory
from django.urls import path, include

from django_early_return import EarlyReturn

from qnc_crud.permissions import assert_permission, not_currently_allowed


def check_for_delete_user(request):
    assert_permission(request, 'auth.delete_user')
    return http.HttpResponse()
def raise_not_allowed(request):
    not_currently_allowed(request, 'registration is not yet open')

urlpatterns = [
    path('', include('qnc_crud.urls')),
    path('check_for_delete_user', check_for_delete_user),
    path('not_currently_allowed', not_currently_allowed),
]
def get_perm_by_name(perm_name):
    app_name, codename = perm_name.split('.', 1)
    return Permission.objects.get(codename=codename, content_type__app_label=app_name)
def log_in_user_with_perms(client, *perms):
    u = User()
    u.save()
    u.user_permissions.set([get_perm_by_name(p) for p in perms])
    u.save()
    client.force_login(u)

@override_settings(
    LOGIN_URL='/login/',
    ROOT_URLCONF='qnc_crud.tests.test_permissions',
    AUTH_USER_MODEL='auth.User',
)
class PermissionsTestCase(TestCase):
    def test_assert_permission_with_no_user(self):
        response = self.client.get('/check_for_delete_user')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response['forbiddenreason'], 'LOGIN_REQUIRED')
        self.assertIn(b'You must be logged in to view this page', response.content)
    def test_assert_permission_with_unpermitted_user(self):
        log_in_user_with_perms(self.client)
        response = self.client.get('/check_for_delete_user')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response['forbiddenreason'], 'PERMISSION_DENIED')
        self.assertIn(b'You do not have the required permissions to view this page', response.content)
    def test_assert_permission_passes(self):
        log_in_user_with_perms(self.client, 'auth.delete_user')
        response = self.client.get('/check_for_delete_user')
        self.assertEqual(response.status_code, 200)

    def test_perm_funcs_can_be_imported_from_qnc_crud(self):
        from qnc_crud import login_required, assert_permission, not_currently_allowed