from django.contrib.auth.models import User
from django.http import Http404
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.permissions import IsOwnerOnly, IsAdminOrPostOnly, IsUserOrReadOnly
from api.serializers import UserSettingsSerializer, UserInfoSerializer, InterestSerializer, EventSerializer, \
    UserSerializer
from feed.models import Interest, Event
from main.models import UserProfile
from main.utils import confirm_password


class UserCreateList(generics.ListCreateAPIView):
    permission_classes = [IsAdminOrPostOnly]
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(is_active=True)


class UserRU(generics.RetrieveUpdateAPIView):
    permission_classes = [IsUserOrReadOnly]
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'id'


class UserSettings(APIView):
    permission_classes = [IsOwnerOnly]

    @staticmethod
    def get_object(pk):
        try:
            return UserProfile.objects.get(user=pk)
        except UserProfile.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        user = self.get_object(request.user.id)
        serializer = UserSettingsSerializer(user)
        return Response(serializer.data)

    def put(self, request, format=None):
        user_id = request.user.id
        user_profile = self.get_object(user_id)
        serializer = UserSettingsSerializer(user_profile, data=request.data)

        if 'current_pass' in request.data['user']:
            current = request.data['user']['current_pass']
            if confirm_password(user_id, current) and serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('Enter Current Password', status=status.HTTP_401_UNAUTHORIZED)


class ProfilePhoto(APIView):
    permission_classes = [IsOwnerOnly]

    def put(self, request, format=None):
        serializer = UserSettingsSerializer(request.user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserInfo(APIView):
    permission_classes = [IsAuthenticated]
    paginate_by = 10
    api_view = ['GET']

    def get(self, request, username=None, *args, **kwargs):
        try:
            if 'related' in kwargs:
                related_user = kwargs['related']
                user = User.objects.get(pk=related_user)
                serializer = UserInfoSerializer(user, context={'request_user': request.user.id})
                return Response(serializer.data)

            user = User.objects.get(username=username)
            serializer = UserInfoSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response('Cannot find User', status=status.HTTP_404_NOT_FOUND)


class SingleUserInterestViewSet(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        interests = Interest.objects.filter(user=user)
        return interests

    def list(self, request, **kwargs):
        queryset = self.get_queryset()
        serializer = InterestSerializer(queryset, many=True)
        return Response(serializer.data)


class UserEventsCreatedView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        events = Event.objects.filter(creator=user)
        return events

    def list(self, request, **kwargs):
        queryset = self.get_queryset()
        serializer = EventSerializer(queryset, many=True)
        return Response(serializer.data)


class UserEventsAttendingView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        events = Event.objects.filter(attendees=user)
        return events

    def list(self, request, **kwargs):
        queryset = self.get_queryset()
        serializer = EventSerializer(queryset, many=True)
        return Response(serializer.data)


class NearUsersView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        users = User.objects.all()
        return users

    def list(self, request, **kwargs):
        queryset = self.get_queryset()
        serializer = UserInfoSerializer(queryset, many=True)
        return Response(serializer.data)
