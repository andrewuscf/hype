from django.contrib.auth.models import User
from django.http import Http404
from rest_framework.exceptions import ValidationError
from models import UserProfile


def create_profile(sender, instance, signal, created, **kwargs):
    """creating a profile when a user is created"""
    if created:
        UserProfile(user=instance).save()


def confirm_password(pk, current_password):
    try:
        user = User.objects.get(pk=pk)
        if user.check_password(current_password):
            return True
        else:
            raise ValidationError({'current_password': 'Is Incorrect'})
    except User.DoesNotExist:
        raise Http404


def change_password(pk, new_pass, repeat_pass):
    user = User.objects.get(pk=pk)
    if new_pass == repeat_pass:
        user.set_password(new_pass)
    else:
        raise ValidationError({'password': 'Does Not Match'})

