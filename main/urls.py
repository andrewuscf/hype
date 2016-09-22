from django.conf.urls import url

import views


urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^user/(?P<username>[\w.@+-]+)/$', views.profile, name='profile'),
    url(r'^settings/$', views.settings, name='settings'),
    url(r'^privacy/$', views.privacy, name='privacy'),
]
