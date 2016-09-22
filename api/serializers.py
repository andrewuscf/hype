from django.contrib.auth.models import User
from rest_framework import serializers

from allauth.socialaccount.models import SocialAccount
from rest_framework.validators import UniqueValidator

from feed.models import Image, Tag, Event, Category, Interest
from feed.models import Request
from main.models import UserProfile, UserPhotos, ReportUser, HideUser


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('url',)


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request


class GenericRelatedField(serializers.Field):
    def to_representation(self, value):
        if isinstance(value, Request):
            return RequestSerializer(value).data
        if isinstance(value, Image):
            return ImageSerializer(value).data
        # Not found - return string.
        return str(value)


class UserProfileSerializer(serializers.ModelSerializer):
    avatar_url = serializers.CharField(required=False)
    date_of_birth = serializers.DateField(write_only=True)
    bio = serializers.CharField(required=False, allow_blank=True)
    age = serializers.IntegerField(read_only=True)

    class Meta:
        model = UserProfile


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(validators=[UniqueValidator(queryset=User.objects.all())])
    profile = UserProfileSerializer(read_only=True)

    def create_or_update_profile(self, user, profile_data):
        profile, created = UserProfile.objects.get_or_create(userprofile=user, defaults=profile_data)
        if not created and profile_data is not None:
            super(UserSerializer, self).update(profile, profile_data)

    def create(self, validated_data):
        profile = validated_data.pop('profile')
        user = User.objects.create(**validated_data)
        self.create_or_update_profile(user, profile)
        return user

    def update(self, instance, validated_data):
        profile = validated_data.pop('profile')
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.avatar_url = validated_data.get('avatar_url', instance.avatar_url)
        instance.username = validated_data.get('username', instance.username)
        instance.profile.date_of_birth = profile.get('date_of_birth', instance.date_of_birth)
        instance.profile.avatar_url = profile.get('avatar_url', instance.avatar_url)
        instance.profile.bio = profile.get('bio', instance.bio)
        instance.profile.save()
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'profile')


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name',)


class EventSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, default=serializers.CurrentUserDefault())
    attendees = UserSerializer(many=True, read_only=True)

    title = serializers.CharField(max_length=120)
    location = serializers.CharField(max_length=255)
    start = serializers.DateTimeField()
    end = serializers.DateTimeField()
    splash_art = serializers.ImageField(required=False)
    icon = serializers.ImageField(required=False)

    latitude = serializers.FloatField(read_only=True)
    longitude = serializers.FloatField(read_only=True)

    class Meta:
        model = Event
        fields = ('id', 'user', 'title', 'location', 'start', 'end',
                  'splash_art', 'attendees', 'latitude', 'longitude', 'icon')


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=100)

    class Meta:
        model = Category
        fields = ('name',)


class InterestSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    images = ImageSerializer(source='images.filter', many=True, read_only=True)

    class Meta:
        model = Interest
        fields = ('name', 'images', 'category')


class UserPhotosSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPhotos
        fields = ('image',)


class ReportUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportUser


class HideUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = HideUser
        fields = ('current_user', 'hidden_users')


class UserInfoSerializer(serializers.ModelSerializer):
    similar = serializers.SerializerMethodField(read_only=True)
    photos = UserPhotosSerializer(source='userphotos_set', many=True, read_only=True)
    interests = InterestSerializer(source='interest_set', many=True, read_only=True)
    profile = UserProfileSerializer(read_only=True)
    connected = serializers.SerializerMethodField(read_only=True)

    def __init__(self, *args, **kwargs):
        kwargs.pop('password', None)
        super(UserInfoSerializer, self).__init__(*args, **kwargs)

    def get_connected(self, obj):
        social_accounts = SocialAccount.objects.filter(user=obj)
        accounts = {}
        for account in social_accounts:
            if account.provider not in accounts:
                accounts[account.provider] = True
        return accounts

    def get_similar(self, obj):
        if 'request_user' in self.context:
            query = Interest.objects.filter(user=obj).filter(user=self.context['request_user'])
            return InterestSerializer(query, many=True).data
        return {}

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'photos', 'interests', 'profile',
                  'is_active', 'similar', 'connected')


class UserSettingsSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    bio = serializers.CharField(required=False, allow_blank=True, )
    avatar_url = serializers.CharField(required=False, allow_blank=True, read_only=True)
    age = serializers.IntegerField(required=False, allow_null=True)

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user = instance.user
        user.username = user_data.get('username', user.username)
        user.first_name = user_data.get('first_name', user.first_name)
        user.last_name = user_data.get('last_name', user.last_name)

        instance.bio = validated_data.get('bio', instance.bio)
        instance.avatar_url = validated_data.get('avatar_url', instance.avatar_url)
        instance.age = validated_data.get('age', instance.age)

        instance.save()
        user.save()
        return instance

    class Meta:
        model = UserProfile
        fields = ('bio', 'avatar_url', 'age', 'user')


class UserProfilePhotoSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    avatar_url = serializers.CharField(required=False, allow_blank=True, read_only=True)

    class Meta:
        model = UserProfile
        fields = ('avatar_url', 'user')
