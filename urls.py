from django.conf.urls.defaults import patterns, include, url
import subscribe.urls

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^subscribe/', include(subscribe.urls)),
)
