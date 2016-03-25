from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from django.contrib.admin import forms as admin_forms
from django.conf import settings
from accounts import views, forms


urlpatterns = [
    url(r'^logout/$', auth_views.logout),
    url(r'^login/staff/$', views.login_staff, name='login_staff'),
    url(r'^register/candidate/$', views.Register.as_view(), name='register_candidate'),
]
