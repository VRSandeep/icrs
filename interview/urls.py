from django.conf.urls import url, include
from . import views


urlpatterns = [
    url(r'^rating/add/$', views.RatingCreateUpdate.as_view()),
]
