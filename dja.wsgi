#!/usr/bin/python
import os
import sys

if '/var/www/html/quiz' not in sys.path:
	sys.path.append('/var/www/html/quiz')
if '/var/www/html' not in sys.path:
	sys.path.append('/var/www/html')

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
