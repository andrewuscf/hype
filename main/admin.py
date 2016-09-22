from django.contrib import admin
from main.models import *

defaultImages = 3

admin.site.register(LocationCurrent)
admin.site.register(UserProfile)
admin.site.register(HideUser)
admin.site.register(ReportUser)
admin.site.register(UserPhotos)


