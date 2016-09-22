from __future__ import unicode_literals

from django.apps import AppConfig


class FeedConfig(AppConfig):
    name = 'feed'

    def ready(self):
        from feed.signals import facebook_receiver, add_spotify, add_instagram, add_youtube, remove_fb, remove_spotify, \
            remove_instagram, remove_youtube
        from allauth.socialaccount.signals import social_account_added, social_account_removed

        # Might need to do this when user logins in. user_logged_in
        social_account_added.connect(receiver=facebook_receiver)
        social_account_added.connect(receiver=add_spotify)
        social_account_added.connect(receiver=add_instagram)
        social_account_added.connect(receiver=add_youtube)

        social_account_removed.connect(receiver=remove_fb)
        social_account_removed.connect(receiver=remove_spotify)
        social_account_removed.connect(receiver=remove_instagram)
        social_account_removed.connect(receiver=remove_youtube)
