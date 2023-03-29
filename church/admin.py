from django.contrib import admin

from .models import Sermon

from image_cropping import ImageCroppingMixin

# Register your models here.
@admin.register(Sermon)
class SermonAdmin(ImageCroppingMixin, admin.ModelAdmin):
    list_display = ('title', 'preacher', 'status', 'publish')
    list_filter = ('status', 'created', 'publish', 'preacher')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')
    