from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('website.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^voting/', include('interview.urls')),
]

admin.site.site_header = 'Interviewers Administration'
admin.site.index_title = 'Interview Candidate Rating System (ICRS)'
admin.site.site_title = 'ICRS Administration'
