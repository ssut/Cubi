import os
import site
import sys

site.addsitedir('/usr/local/lib/python2.7/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'tinicube.settings'
os.environ['DJANGO_PRODUCTION'] = '1'

sys.path.insert(0, '/var/www/tinicube/webroot')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
