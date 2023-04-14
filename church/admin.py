from django.contrib import admin

from .models import Sermon, Event, ChildDedication, PrayerRequest, NewBeleiver, Testimony, Career, MpesaPayment, CardPayment
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
    
    
@admin.register(Event)
class EventAdmin(ImageCroppingMixin, admin.ModelAdmin):
    list_display = ('title', 'organizer', 'status', 'publish')
    list_filter = ('status', 'created', 'publish', 'organizer')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')
    
@admin.register(ChildDedication)
class ChildDedicationAdmin(admin.ModelAdmin):
    list_display = ('child_name', 'child_date_of_birth', 'date_of_dedication', 
                    'mothers_name', 'fathers_name', 'dedication_status', 'created')
    list_filter = ('child_gender', 'dedication_status', 'created')
    search_fields = ('child_name', 'mothers_name', 'fathers_name')
    date_hierarchy = 'created'
    ordering = ('created',)
    

@admin.register(PrayerRequest)
class PrayerRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'title', 'content', 'prayer_status', 'created')
    list_filter = ('prayer_status', 'created')
    search_fields = ('name', 'title', 'content')
    date_hierarchy = 'created'
    ordering = ('created',)
    
@admin.register(NewBeleiver)
class NewBeleiverAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'residential_area', 'current_church', 'created')
    search_fields = ('name', 'current_church')
    date_hierarchy = 'created'
    ordering = ('created',)
    
    
@admin.register(Testimony)
class TestimonyAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'title', 'created')
    search_fields = ('name', 'content',)
    date_hierarchy = 'created'
    ordering = ('created',)
    

@admin.register(Career)
class CareerAdmin(admin.ModelAdmin):
    list_display = ('title', 'status','deadline', 'publish')
    list_filter = ('status', 'created', 'publish', 'deadline')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')
    
    
@admin.register(MpesaPayment)
class MpesaPaymentAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'amount', 'status', 'created_at','purpose')
    list_filter = ('purpose', )
    search_fields = ('phone_number', )
    date_hierarchy = 'created_at'
    ordering = ('created_at',)
    
    
@admin.register(CardPayment)
class CardPaymentAdmin(admin.ModelAdmin):
    list_display = ('braintree_id', 'holder_name', 'phone_number', 'amount', 'status', 'purpose', 'created_at')
    search_fields = ('phone_number', )
    date_hierarchy = 'created_at'
    ordering = ('created_at',)
    

        