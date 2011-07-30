from django.conf.urls.defaults import patterns, url

from glitchtools.users import views

urlpatterns = patterns('',
    url(r'^token/', views.token, name='glitchtools-users-token'),
    url(r'^logout/', 'django.contrib.auth.views.logout', name='glitchtools-users-logout', kwargs={'next_page': '/', 'redirect_field_name': 'next'}),
    url(r'', views.login, name='glitchtools-users-login'),
)
