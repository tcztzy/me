from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings

urlpatterns = [
    url(r'', include('blog.urls', namespace='blog'))
]

if settings.DEBUG:
    urlpatterns = [
        url(r'^admin/', admin.site.urls),
    ] + urlpatterns
