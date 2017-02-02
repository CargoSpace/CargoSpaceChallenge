# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from cms.sitemaps import CMSSitemap
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static

admin.autodiscover()
	
urlpatterns = [
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap',
        {'sitemaps': {'cmspages': CMSSitemap}}),
    url(r'^select2/', include('django_select2.urls')),
    url(r'^invitations/', include('invitations.urls', namespace='invitations')),
]

urlpatterns += [
    url(r'^', include('app.urls')),
    url(r'^dashboard/', include('dashboard.urls')),
    url(r'^cschallenge/', include('acm.urls')),
    url(r'^accounts/', include('allauth.urls')), #django-allauth
    url(r'^taggit_autosuggest/', include('taggit_autosuggest.urls')),    
]

urlpatterns += i18n_patterns('',
	url(r'^pages/', include('pages.urls')),
    url(r'^admin/', include(admin.site.urls)),  # NOQA
    url(r'^', include('cms.urls')),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)