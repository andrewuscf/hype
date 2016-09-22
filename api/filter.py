from django.contrib.auth.models import User
import django_filters
from geopy import Nominatim
import geopy
from geopy.exc import GeocoderTimedOut
import rest_framework_filters as filters
from feed.models import Event


class UserFilter(filters.FilterSet):
    class Meta:
        model = User
        username = filters.CharFilter(name='username')


class PostFilter(django_filters.FilterSet):

    title = django_filters.CharFilter(name='title')
    category = django_filters.ChoiceFilter(name='category')
    date = django_filters.DateFilter(name='date')
    # author = filters.RelatedFilter(UserFilter, name='author')
    # distance = django_filters.CharFilter(action=filter_distance)

#     def filter_distance(queryset, value):
#         if not value:
#             return queryset
#
#         if value:
#             geopy.distance = vincenty()
#             try:
#                 place = ''
#                 place += value
#                 distance =
#             except GeocoderTimedOut:
#                 print("Error")
#             else:
#                 print("No location")
# from geopy.distance import vincenty
# >>> newport_ri = (41.49008, -71.312796)
# >>> cleveland_oh = (41.499498, -81.695391)
# >>> print(vincenty(newport_ri, cleveland_oh).miles)

    class Meta:
            model = Event
            fields = ['title','category', 'date']



