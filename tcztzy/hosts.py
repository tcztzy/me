from django.conf import settings
from django_hosts import host

host_patterns = [
    host(r'blog', settings.ROOT_URLCONF, name='blog')
]
