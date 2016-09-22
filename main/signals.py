from django.contrib.auth.models import User
from main.models import LocationCurrent

from rest_framework.authtoken.models import Token

from models import UserProfile


def set_blank_location(request, user, **kwargs):
    userQuery = User.objects.get(username=user)
    LocationCurrent.objects.create(user=userQuery, active=True)


def check_if_userlocation(request, user, **kwargs):
    userQuery = User.objects.get(username=user)
    if not LocationCurrent.objects.filter(user=userQuery).exists():
        LocationCurrent.objects.create(user=userQuery, active=True)
    else:
        LocationCurrent.objects.filter(user=userQuery).update(active=True)


def user_signed_up_(request, user, sociallogin=None, **kwargs):
    '''
    When a social account is created successfully and this signal is received,
    django-allauth passes in the sociallogin param, giving access to metadata on the remote account, e.g.:
    sociallogin.account.provider  # e.g. 'twitter'
    sociallogin.account.get_avatar_url()
    sociallogin.account.get_profile_url()
    sociallogin.account.extra_data['screen_name']
    See the socialaccount_socialaccount table for more in the 'extra_data' field.
    '''

    if sociallogin:
        # Extract first / last names from social nets and store on User record
        if sociallogin.account.provider == 'instgram':
            name = sociallogin.account.extra_data['insta_profile']['data']['full_name']
            user.first_name = name.split()[0]
            user.last_name = name.split()[1]

        if sociallogin.account.provider == 'spotify':
            name = sociallogin.account.extra_data['spot_profile']['display_name']
            user.first_name = name.split()[0]
            user.last_name = name.split()[1]

        if sociallogin.account.provider == 'facebook':
            data = sociallogin.account.extra_data
            user.first_name = data['first_name']
            user.last_name = data['last_name']

        if sociallogin.account.provider == 'google':
            try:
                user.first_name = sociallogin.account.extra_data['google_profile']['given_name']
                user.last_name = sociallogin.account.extra_data['google_profile']['family_name']
            except KeyError:
                user.first_name = sociallogin.account.extra_data['google_profile']['name']

        user.save()


def user_logged_in_(request, user, sociallogin=None, **kwargs):
    '''
    On successful social login (not signup), refresh profile details etc.
    For new users, create profile first!
    '''
    p, created = UserProfile.objects.get_or_create(user=user)  # 'created' will be true or false
    p.set_avatar_url(p)


def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
