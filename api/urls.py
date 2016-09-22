from django.conf.urls import include, url
from api.views import events, user

user_patterns = [
    url(r'^$', user.UserCreateList.as_view()),
    url(r'^(?P<id>\d+)/$', user.UserRU.as_view()),

    url(r'^settings/', user.UserSettings.as_view()),
    url(r'^info/(?P<username>[\w.@+-]+)', user.UserInfo.as_view()),
    url(r'^interests/', user.SingleUserInterestViewSet.as_view()),
    url(r'^related/(?P<related>[0-9]+)/', user.UserInfo.as_view()),
    url(r'^near/', user.NearUsersView.as_view()),
    url(r'^events/attending/', user.UserEventsAttendingView.as_view()),
    url(r'^events/created/', user.UserEventsCreatedView.as_view()),
    url(r'^profile/photo/', user.ProfilePhoto.as_view()),
]

events_patterns = [
    url(r'^$', events.EventCreate.as_view()),
    url(r'^list/$', events.EventList.as_view()),
    url(r'^(?P<pk>\d+)/$', events.EventDetail.as_view()),
]

urlpatterns = [
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^event/', include(events_patterns)),
    url(r'^user/', include(user_patterns)),
]
