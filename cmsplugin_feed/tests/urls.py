from django.conf.urls import patterns, url, include
from django.contrib import admin


urlpatterns=patterns('',
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('cms.urls')),
)
