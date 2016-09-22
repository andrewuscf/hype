from urllib2 import urlopen
from simplejson import loads

from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import User

from feed.models import Category, Interest
from feed.utils import fb_data, interest_insert_update
from main.models import UserPhotos


def getAdditionalData(link):
    content = loads(urlopen(link).read())
    try:
        if content['paging']['next']:
            print content['paging']['next']
            getAdditionalData(content['paging']['next'])
    except KeyError:
        print content['data']


def facebook_receiver(request, sociallogin=None, **kwargs):
    print sociallogin.account.extra_data
    user_info = SocialAccount.objects.filter(user=request.user.id, provider='facebook')
    subjects = ['music', 'books', 'likes', 'sports']
    # If signal is from facebook.
    test = 0
    if user_info:
        user = User.objects.get(pk=request.user.id)
        #     get prestion info
        for person in user_info:
            if person.extra_data['likes']['paging']['next']:
                getAdditionalData(person.extra_data['likes']['paging']['next'])
                # for each in  person.extra_data['likes']['data']:
                #     test +=1
                #     print test

                # facebook music
                # for subject in subjects:
                # fb_data(person.extra_data['fb_info'][subject]['data'], user)


def add_spotify(request, sociallogin=None, **kwargs):
    user_info = SocialAccount.objects.filter(user=request.user.id, provider='spotify')

    if user_info:
        user = User.objects.get(pk=request.user.id)
        for person in user_info:
            for items in person.extra_data['spot_info']['items']:
                photos = []
                music = {k: v for (k, v) in items.iteritems() if 'track' in k}
                for k, d in music.iteritems():
                    track = d

                    for x in range(0, 1):
                        try:
                            photos.append(track['album']['images'][x]['url'])
                        except IndexError:
                            pass

                    artist = track['artists'][00]['name']

                    interest_insert_update(user, artist, photos, 'Music', 'Spotify')


def add_instagram(request, sociallogin=None, **kwargs):
    accounts = SocialAccount.objects.filter(user=request.user.id, provider='instagram')
    if accounts:
        for person in accounts:
            for items in person.extra_data['insta_info']['data']:
                images = {k: v for (k, v) in items.iteritems() if 'images' in k}
                for key, value in images.iteritems():
                    img = value

                    img_link = img['standard_resolution']['url']

                    # check if interest exists and add user or all interest
                    if UserPhotos.objects.filter(image=img_link).exists():
                        pass
                    else:
                        user = User.objects.get(pk=person.user.id)
                        UserPhotos.objects.create(image=img_link, user=user)


def add_youtube(request, sociallogin=None, **kwargs):
    accounts = SocialAccount.objects.filter(user=request.user.id, provider='google')
    if accounts:
        # put music category if not in database
        if not Category.objects.filter(name='Subscriptions').exists():
            Category.objects.create(name='Subscriptions')

        for person in accounts:
            for items in person.extra_data['youtube_info']['items']:
                photos = []
                subscribtions = {k: v for (k, v) in items.iteritems() if 'snippet' in k}
                for k, d in subscribtions.iteritems():
                    sub = d

                    photos.append(sub['thumbnails']['high']['url'])

                    name = sub['title']

                    user = User.objects.get(pk=person.user.id)

                    interest_insert_update(user, name, photos, 'Subscriptions', 'Google')


# when user disconnects social account

def remove_fb(request, socialaccount, **kwargs):
    if socialaccount.provider == 'facebook':
        interests = Interest.objects.filter(user=request.user.id, source='Facebook')
        user = User.objects.get(pk=request.user.id)
        for each in interests:
            each.user.remove(user)
    else:
        pass


def remove_spotify(request, socialaccount, **kwargs):
    if socialaccount.provider == 'spotify':
        spotify_music = Interest.objects.filter(user=request.user.id, source='Spotify')
        user = User.objects.get(pk=request.user.id)
        for each in spotify_music:
            each.user.remove(user)
    else:
        pass


def remove_instagram(request, socialaccount, **kwargs):
    if socialaccount.provider == 'instagram':
        photos = UserPhotos.objects.filter(user=request.user.id)
        photos.delete()
    else:
        pass


def remove_youtube(request, socialaccount, **kwargs):
    if socialaccount.provider == 'google':
        subscriptions = Interest.objects.filter(user=request.user.id, source='Google')
        user = User.objects.get(pk=request.user.id)
        for each in subscriptions:
            each.user.remove(user)
    else:
        pass
