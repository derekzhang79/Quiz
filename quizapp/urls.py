from django.conf.urls.defaults import *
from django.conf import settings
from os.path import dirname

urlpatterns = patterns('',
	url(r'^$', 'quizapp.views.quizlist', name='quizlist'),
	url(r'^quiz/(?P<id>\d+)$', 'quizapp.views.quizinfo', name='quizinfo'),
	url(r'^quiz/(?P<id>\d+)/do$', 'quizapp.views.doquiz', name='doquiz'),
	url(r'^quiz/(?P<id>\d+)/send$', 'quizapp.views.sendquiz', name='sendquiz'),
	url(r'^quiz/(?P<id>\d+)/(?P<notused>\d+)-(?P<resid>\d+)-(?P<code>[A-Z0-9]+)$', 'quizapp.views.result', name='result'),
	url (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': dirname(__file__)+'/static',  'show_indexes': settings.DEBUG}, "static"),
)
