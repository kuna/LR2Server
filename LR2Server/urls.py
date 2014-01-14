from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'LR2Server.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    # -- https://docs.djangoproject.com/en/dev/topics/http/urls/

    #url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'LR2Server.views.main'),
    url(r'^(?P<index>\d+)/$', 'LR2Server.views.page'),
    url(r'^user/(?P<user>\w+)/$', 'LR2Server.views.score'),
    url(r'^downbms/(?P<index>\d+)/$', 'LR2Server.views.downloadBMS'),
    url(r'^downsabun/(?P<index>\w+)/$', 'LR2Server.views.downloadSabun'),
    url(r'^downmusic/(?P<index>\w+)/$', 'LR2Server.views.downloadMusic'),
    url(r'^(?P<path>.*)$', 'django.views.static.serve', {'document_root': BASE_DIR+'/LR2Server/templates'}),
)
