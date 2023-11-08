from django.db import models
from django.utils import timezone
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
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
    feature_img = models.ImageField(
        blank=True, null=True, upload_to='feature_img/')
    preacher = models.CharField(max_length=50)
    readings = models.CharField(max_length=200)
    content = RichTextUploadingField()
    created = models.DateTimeField(auto_now_add=True)
    publish = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='draft')

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
    feature_img = models.ImageField(
        blank=True, null=True, upload_to='feature_img/')
    content = RichTextUploadingField()
    organizer = models.CharField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    commence_date = models.DateTimeField(blank=True, null=True)
    ending_date = models.DateTimeField(blank=True, null=True)
    entry_fee = models.DecimalField(
        decimal_places=0, max_digits=5, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    publish = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='draft')

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


class Career(models.Model):
    STATUS_CHOICES = (
        ('draft', 'draft'),
        ('publish', 'publish')
    )
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique_for_date='publish')
    content = RichTextUploadingField()
    created = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(auto_now_add=True)
    publish = models.DateTimeField(default=timezone.now)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='draft')

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('church:career_detail', args=[self.publish.year,
                                                     self.publish.month,
                                                     self.publish.day,
                                                     self.slug])


class MpesaPayment(models.Model):
    """Model definition for MpesaPayment."""
    receipt_number = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    amount = models.FloatField()
    date = models.DateTimeField(auto_now_add=False)
    status = models.BooleanField(default=False)

    class Meta:
        """Meta definition for MpesaPayment."""
        verbose_name = 'MpesaPayment'
        verbose_name_plural = 'MpesaPayments'
        ordering = ('-date',)

    def __str__(self):
        """Unicode representation of MpesaPayment."""
        return self.receipt_number


class CardPayment(models.Model):
    braintree_id = models.CharField(max_length=200)
    holder_name = models.CharField(max_length=200)
    phone_number = PhoneNumberField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    purpose = models.CharField(max_length=200)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    class Meta:
        verbose_name = 'Card Payment'
        verbose_name_plural = 'Card Payments'

    def __str__(self):
        return self.holder_name
