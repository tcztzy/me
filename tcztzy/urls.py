from django.conf.urls import url
from django.contrib import admin
from django.conf import settings

urlpatterns = [
    
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^admin/', admin.site.urls),
    ]
