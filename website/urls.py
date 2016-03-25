from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^interviewer/$', views.interviewer),
    url(r'^candidate/$', views.candidate),
]
