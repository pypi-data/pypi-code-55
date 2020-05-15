from django.urls import include
from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from djangopollapp.api.v1.views import PollView, QuestionView

router = DefaultRouter()
router.register(r'^polls', PollView, basename='PollView')
router.register(r'^questions', QuestionView, basename='QuestionView')

urlpatterns = [
    url(r'^', include(router.urls))
]