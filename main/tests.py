from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from main.forms import UserForm


class CreatingUserTestCase(TestCase):
    def test_clean_username_exception(self):
        User.objects.create_user(username='test', email='andrew@hotmail.com', password='letmein')

        form = UserForm()

        with self.assertRaises(ValidationError):
            form.clean_username()
