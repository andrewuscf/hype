from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from geopy import Point

from allauth.account.models import EmailAddress

from socialplug.settings import STATIC_URL

_SCORE_TYPE_CHOICES = (
    (2, 'Love'),
    (1, 'Like'),
    (.5, 'Ok'),
    (-1, 'Dislike'),
    (-2, 'Bad'),
)


class Vote(models.Model):
    content_type = models.ForeignKey(ContentType, related_name="updown_votes")
    object_id = models.PositiveIntegerField()
    score = models.SmallIntegerField(choices=_SCORE_TYPE_CHOICES)
    user = models.ForeignKey(User, related_name="updown_votes")
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    content_object = GenericForeignKey()

    class Meta:
        unique_together = ('content_type', 'object_id', 'user')

    def __unicode__(self):
        display_string = "{user} voted {score} on {content_object}" \
            .format(user=self.user.username, score=self.score, content_object=self.content_object)
        return display_string


class UserPhotos(models.Model):
    image = models.CharField(max_length=300)
    user = models.ForeignKey(User)

    class Meta:
        db_table = 'photos'

    def __unicode__(self):
        return self.user.username


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    date_of_birth = models.DateField()
    bio = models.TextField(help_text='Tell us about You', blank=True, max_length=500)
    avatar_url = models.CharField(default=STATIC_URL + 'img/user-avatar.png', max_length=255, blank=True, null=True)
    age = models.IntegerField(null=True, blank=True)
    rep = GenericRelation(Vote)

    # setting avatar url based on social or local auth
    def calculate_age(self):
        today = timezone.now()
        print self.date_of_birth
        self.age = today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        self.save()

    def set_avatar_url(self):
        if self.user.socialaccount_set.all().count() > 0:
            sa = self.user.socialaccount_set.all()[0]
            img_url = None
            if sa.provider == "google":
                img_url = sa.extra_data['google_profile']['picture']

            elif sa.provider == "spotify":
                img_url = sa.extra_data['spot_profile']['images'][0]['url']

            elif sa.provider == "facebook":
                img_url = "http://graph.facebook.com/{uid}/picture?type=large".format(uid=str(sa.uid))

            elif sa.provider == "instagram":
                img_url = sa.extra_data['insta_profile']['data']['profile_picture']

            else:
                pass

            self.avatar_url = img_url
            self.save()

    def display_name(self):
        if self.user.first_name and self.user.last_name:
            display_string = "{first} {last}".format(
                first=self.user.first_name,
                last=self.user.last_name)
        elif self.user.first_name and not self.user.last_name:
            display_string = "{first}".format(
                first=self.user.first_name)
        else:
            display_string = "{uname}".format(
                uname=self.user.username)

        return display_string

    class Meta:
        db_table = 'user_profile'

    def account_verified(self):
        result = EmailAddress.objects.filter(email=self.user.email)
        if len(result):
            return result[0].verified
        return False

    User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

    def __unicode__(self):
        display_string = "{display} ({username})".format(display=self.display_name(), username=self.user.username)
        return display_string

    # def save(self, *args, **kwargs):
    #     self.calculate_age()
    #     super(UserProfile, self).save(*args, **kwargs)


class ReportUser(models.Model):
    reporter = models.ForeignKey(User, related_name='reporter')
    being_reported = models.ForeignKey(User, related_name='being_reported')
    reason = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)


class HideUser(models.Model):
    current_user = models.ForeignKey(User, related_name='from_user')
    hidden_users = models.ManyToManyField(User, related_name='hide_user')
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.current_user.username

    class Meta:
        db_table = 'hidden_users'


class LocationCurrent(models.Model):
    user = models.ForeignKey(User)
    latitude = models.FloatField(null=True, default=0)
    longitude = models.FloatField(null=True, default=0)
    active = models.BooleanField(default=False)

    address = models.CharField(null=True, max_length=120, blank=True)
    city = models.CharField(null=True, max_length=60, blank=True)
    zip_code = models.CharField(null=True, max_length=10, blank=True)

    created = models.DateTimeField(auto_now_add=True, )
    updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return '{}'.format(self.user)

    @property
    def coordinates(self):
        return Point(self.longitude, self.latitude)
