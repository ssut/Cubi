from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cubi.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    
    url(r'^django_admin/', include(admin.site.urls)),
)
