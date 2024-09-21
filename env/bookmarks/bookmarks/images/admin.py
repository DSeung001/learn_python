from distutils.command.clean import clean

from django.contrib import admin
from images.models import Image


# Register your models here.
@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['title','slug','image','created']
    list_filter = ['created']