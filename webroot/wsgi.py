import os
import sys
import site

#site.addsitedir('/home/pahkey/virtualenv/codejob/lib/python2.7/site-packages')
site.addsitedir('/usr/local/lib/python2.7/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'tinicube.settings'
os.environ['DJANGO_PRODUCTION'] = '1'

sys.path.insert(0, '/srv/www/tinicube/webroot')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
