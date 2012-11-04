# -*- coding: utf-8 -*
from django.conf.urls import patterns
from django.conf.urls import url

urlpatterns = patterns('newsletter.views',
	# Subscribe
	url(r'^subscribe/$', 'subscribe', name='subscribe'),
	# Confirm, UnSubscribe, Setting
	# http://ronis.de.glav.it/newsletter/settings/1888357bf967131e940fd76ea5e166b5/
	url(r'^settings/(?P<key>[0-9a-f]{32})/$', 'settings', name='settings'),
)
