from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^new/$', 'subscribe.views.new'),
    url(r'^(?P<action>(activate|deactivate))/(?P<subscribe_id>.+)/(?P<token>[a-zA-Z0-9]+)/$', 'subscribe.views.manage'),
)