from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from django.contrib.admin import forms as admin_forms
from django.conf import settings
from accounts import views, forms


urlpatterns = [
    # url(r'^', include('django.contrib.auth.urls')),
    # url(r'^login/$', auth_views.login),
    url(r'^logout/$', auth_views.logout),
    # url(r'^password_change/$',  auth_views.password_change),
    # url(r'^password_change/done/$',  auth_views.password_change_done),
    # url(r'^password_reset/$',  auth_views.password_reset),
    # url(r'^password_reset/done/$',  auth_views.password_reset_done),
    # url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.password_reset_confirm),
    # url(r'^reset/done/$', auth_views.password_reset_complete),

    url(r'^staff_login/$', auth_views.login, {
        'authentication_form': admin_forms.AdminAuthenticationForm,
        'template_name': 'accounts/login.html',
        'redirect_field_name': settings.LOGIN_URL
    }, name='login'),
    url(r'^login/staff/$', views.login_staff, name='login_staff'),
    url(r'^register/candidate/$', views.register_candidate, name='register_candidate'),
]
