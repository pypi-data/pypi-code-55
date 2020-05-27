from django.urls import path
from django.views.generic.base import RedirectView

from .admin_site import sarscov2_admin

app_name = "sarscov2"

urlpatterns = [
    path("admin/", sarscov2_admin.urls),
    path("", RedirectView.as_view(url="/sarscov2/admin/"), name="home_url"),
]
