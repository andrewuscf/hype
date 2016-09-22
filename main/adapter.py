from django.conf import settings
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def get_connect_redirect_url(self, request, socialaccount):
        path = '/users/{username}/'
        assert request.user.is_authenticated()
        return path.format(username=request.user.username)
