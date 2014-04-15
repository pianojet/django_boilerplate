from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('app.common.views',
    url(r'^$', 'index', name='common_index'),    
    url(r'^login/$', 'login', name='common_login'),    
    url(r'^logout/$', 'logout', name='common_logout'),
    url(r'^signup/', 'sign_up', name='common_signup'),

)