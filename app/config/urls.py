from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('app.config.views',
    url(r'^password-change/$', 'django.contrib.auth.views.password_change', {'template_name': 'common/password_change.html', 'password_change_form' : UfePasswordChangeForm}, name='password_change'),
    url(r'^password-change/done/$', 'django.contrib.auth.views.password_change_done', {'template_name': 'common/password_change_done.html', }, name='password_change_done'),
    url(r'^password-reset/$', 'django.contrib.auth.views.password_reset', {'template_name': 'common/password_reset.html', 'password_reset_form': AdonPasswordResetForm, }, name='password_reset',),
    url(r'^reset/(?P<uidb36>[0-9A-Za-z]+)/(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', {'template_name': 'common/password_reset_confirm.html',
        'set_password_form': UfeSetPasswordForm }, name='password_reset_confirm'),
    url(r'^password-reset/done/$', 'django.contrib.auth.views.password_reset_done', {'template_name': 'common/password_reset_done.html'}, name='password_reset_done'),
    url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete', {'template_name': 'common/password_reset_complete.html'}, name='password_reset_complete'),
)



 