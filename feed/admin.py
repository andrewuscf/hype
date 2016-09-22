from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from feed.models import *

# Register your models here.
admin.site.register(Category)

defaultImages = 3


class ImageInline(GenericTabularInline):
    model = Image
    extra = defaultImages


class ImageAdmin(admin.ModelAdmin):
    inlines = [ImageInline, ]


admin.site.register(Interest, ImageAdmin)
admin.site.register(Event, ImageAdmin)
