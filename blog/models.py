from urllib.parse import urlparse

from django.conf import settings
from django.core.cache import caches
from django.db import models
from django.test import RequestFactory
from django.utils import timezone
from django.utils.cache import _generate_cache_header_key
from django.utils.translation import ugettext_lazy as _
from django_hosts.resolvers import reverse


class EntryQuerySet(models.QuerySet):
    def published(self):
        return self.active().filter(pub_date__lte=timezone.now())

    def active(self):
        return self.filter(is_active=True)


CONTENT_FORMAT_CHOICES = (
    ('reST', 'reStructuredText'),
    ('html', 'Raw HTML'),
    ('markdown', 'Markdown'),
)


class Entry(models.Model):
    headline = models.CharField(max_length=200)
    slug = models.SlugField(unique_for_date='pub_date')
    is_active = models.BooleanField(
        help_text=_(
            "Tick to make this entry live (see also the publication date). "
            "Note that administrators (like yourself) are allowed to preview "
            "inactive entries whereas the general public aren't."
        ),
        default=False,
    )
    pub_date = models.DateTimeField(
        verbose_name=_("Publication date"),
        help_text=_(
            "For an entry to be published, it must be active and its "
            "publication date must be in the past."
        ),
    )
    content_format = models.CharField(choices=CONTENT_FORMAT_CHOICES, max_length=50)
    summary = models.TextField()
    summary_html = models.TextField()
    body = models.TextField()
    body_html = models.TextField()
    author = models.CharField(max_length=100)

    objects = EntryQuerySet.as_manager()

    class Meta:
        db_table = 'blog_entries'
        verbose_name_plural = 'entries'
        ordering = ('-pub_date',)
        get_latest_by = 'pub_date'

    def __str__(self):
        return self.headline

    def get_absolute_url(self):
        kwargs = {
            'year': self.pub_date.year,
            'month': self.pub_date.strftime('%b').lower(),
            'day': self.pub_date.strftime('%d').lower(),
            'slug': self.slug,
        }
        return reverse('weblog:entry', kwargs=kwargs)

    def is_published(self):
        """
        Return True if the entry is publicly accessible.
        """
        return self.is_active and self.pub_date <= timezone.now()
    is_published.boolean = True

    def save(self, *args, **kwargs):
        if self.content_format == 'html':
            self.summary_html = self.summary
            self.body_html = self.body
        elif self.content_format == 'reST':
            # TODO: Add support for reST
            pass
        elif self.content_format == 'markdown':
            # TODO: Add support for Markdown
            pass
        super(Entry, self).save(*args, **kwargs)
        self.invalidate_cached_entry()

    def invalidate_cached_entry(self):
        url = urlparse(self.get_absolute_url())
        rf = RequestFactory(
            SERVER_NAME=url.netloc,
            HTTP_X_FORWARDED_PROTOCOL=url.scheme,
        )
        is_secure = url.scheme == 'https'
        request = rf.get(url.path, secure=is_secure)
        request.LANGUAGE_CODE = 'en'
        cache = caches[settings.CACHE_MIDDLEWARE_ALIAS]
        cache_key = _generate_cache_header_key(settings.CACHE_MIDDLEWARE_KEY_PREFIX, request)
        cache.delete(cache_key)
