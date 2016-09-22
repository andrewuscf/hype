from django.conf.urls import include, url
from django.contrib import admin
from rest_framework.authtoken import views

admin.autodiscover()

urlpatterns = [

    # Urls that need to be gone through

    url(r'^accounts/', include('allauth.urls')),

    # the include, admin, search, and privacy policy
    url(r'^api/v1/', include('api.urls')),
    url(r'^api-token/$', views.obtain_auth_token),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^', include('main.urls')),
    url(r'^', include('feed.urls')),

]

# if settings.DEBUG:
#     urlpatterns += [
#         url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
#     ]
