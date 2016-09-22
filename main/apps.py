from __future__ import unicode_literals

from django.apps import AppConfig


class MainConfig(AppConfig):
    name = 'main'

    def ready(self):
        from allauth.account.signals import user_signed_up, user_logged_in
        from django.conf.global_settings import AUTH_USER_MODEL
        from django.db.models.signals import post_save

        from main.signals import set_blank_location, user_signed_up_, check_if_userlocation, user_logged_in_, \
            create_auth_token
        from main.utils import create_profile
        user_signed_up.connect(receiver=set_blank_location)
        user_signed_up.connect(receiver=user_signed_up_)
        user_logged_in.connect(receiver=check_if_userlocation)
        post_save.connect(receiver=create_profile, sender=AUTH_USER_MODEL)
        user_logged_in.connect(receiver=user_logged_in_)
        post_save.connect(receiver=create_auth_token, sender=AUTH_USER_MODEL)
