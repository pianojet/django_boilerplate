from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('app.common.views',
    url(r'^$', 'home', name='common_home'),
)