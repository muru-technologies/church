from django.db import models
from django.utils import timezone
from django.urls import reverse

from ckeditor_uploader.fields import RichTextUploadingField
from image_cropping import ImageRatioField, ImageCropField


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