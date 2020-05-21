from django.urls import path
from qnc_crud.views.login import LoginView, LogoutView

urlpatterns = [
    path('login/', LoginView.as_view(), name="qnc_crud_login"),
    path('logout/', LogoutView.as_view(), name="qnc_crud_logout"),
    # TODO - forgot password
]