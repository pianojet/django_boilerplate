from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'django.views.generic.simple.redirect_to', {'url': '/public/'}),
    url(r'^public/', include('app.common.urls'))
    url(r'^your/', include('app.config.urls'))
    url(r'^admin/', include(admin.site.urls)),
)