from django.conf.urls import url, include

import views

find_patterns = [
    url(r'^people/$', views.find_friends, name='find_friends'),
    url(r'^events/$', views.find_event, name='find_event'),

]

create_patterns = [
    url(r'^event/$', views.create_event, name='create_event'),
]

urlpatterns = [
    url(r'^find/', include(find_patterns)),
    url(r'^create/', include(create_patterns)),
    url(r'^event/(?P<id>[\w.@+-]+)/$', views.view_event, name='view_event'),
]
