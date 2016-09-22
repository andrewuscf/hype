from rest_framework.test import APIRequestFactory

factory = APIRequestFactory()

request = factory.put('/api/settings/', {'title': 'remember to email dave'})