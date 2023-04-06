from django.db import models
from django.utils import timezone
from django.urls import reverse

from ckeditor_uploader.fields import RichTextUploadingField
from image_cropping import ImageRatioField, ImageCropField
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class Sermon(models.Model):
    STATUS_CHOICES = (
        ('draft', 'draft'),
        ('publish', 'publish')
    )
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique_for_date='publish')
    youtube = models.URLField(blank=True, null=True)
    feature_img = ImageCropField(blank=True, null=True, upload_to='feature_img/')
    # size in w X h
    cropping = ImageRatioField('feature_img', '300x300')
    preacher = models.CharField(max_length=50)
    readings = models.CharField(max_length=200)
    content = RichTextUploadingField()
    created = models.DateTimeField(auto_now_add=True)
    publish = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('church:sermon_detail', args=[self.publish.year,
                                                       self.publish.month,
                                                       self.publish.day,
                                                       self.slug])
        
        
class Event(models.Model):
    STATUS_CHOICES = (
        ('draft', 'draft'),
        ('publish', 'publish')
    )
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique_for_date='publish')
    feature_img = ImageCropField(blank=True, null=True, upload_to='feature_img/')
    # size in w X h
    cropping = ImageRatioField('feature_img', '200x200')
    content = RichTextUploadingField()
    organizer = models.CharField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    commence_date = models.DateTimeField(blank=True, null=True)
    ending_date = models.DateTimeField(blank=True, null=True)
    entry_fee = models.DecimalField(decimal_places=0, max_digits=5, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    publish = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    class Meta:
        ordering = ('-publish',)


    def __str__(self):
        return self.title
    
    
    # def get_absolute_url(self):
    #     return reverse('church:event_detail', args=[self.publish.year,
    #                                                    self.publish.month,
    #                                                    self.publish.day,
    #                                                    self.slug])
    
    
class ChildDedication(models.Model):
    child_name = models.CharField(max_length=200)
    child_gender = models.CharField(max_length=50)
    child_date_of_birth = models.DateField()
    date_of_dedication = models.DateField()
    mothers_name = models.CharField(max_length=200) 
    mothers_contact = PhoneNumberField()
    fathers_name = models.CharField(max_length=200)
    fathers_contact = PhoneNumberField()
    dedication_status = models.BooleanField(default=False)
    created = models.DateTimeField()
    
    class Meta:
        ordering = ('-created',)
        
    
    def __str__(self):
        return self.child_name


class PrayerRequest(models.Model):
    name = models.CharField(max_length=200)
    phone_number = PhoneNumberField()
    title = models.CharField(max_length=200)
    content = models.TextField()
    prayer_status = models.BooleanField(default=False)
    created = models.DateTimeField()
    
    class Meta:
        ordering = ('-created',)
        
    
    def __str__(self):
        return self.name
    
    
class Testimony(models.Model):
    name = models.CharField(max_length=200)
    phone_number = PhoneNumberField()
    title = models.CharField(max_length=200)
    content = models.TextField()
    created = models.DateTimeField()
    
    class Meta:
        ordering = ('-created',)
        
    
    def __str__(self):
        return self.name
    

class NewBeleiver(models.Model):
    name = models.CharField(max_length=200)
    phone_number = PhoneNumberField()
    current_church = models.CharField(max_length=200)
    residential_area = models.CharField(max_length=200)
    created = models.DateTimeField()
    
    class Meta:
        ordering = ('-created',)
        
    
    def __str__(self):
        return self.name
    