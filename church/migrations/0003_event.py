# Generated by Django 4.1.7 on 2023-03-30 08:46

import ckeditor_uploader.fields
from django.db import migrations, models
import django.utils.timezone
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ('church', '0002_sermon_cropping_alter_sermon_feature_img'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=100, unique_for_date='publish')),
                ('feature_img', image_cropping.fields.ImageCropField(blank=True, null=True, upload_to='feature_img/')),
                ('cropping', image_cropping.fields.ImageRatioField('feature_img', '300x300', adapt_rotation=False, allow_fullsize=False, free_crop=False, help_text=None, hide_image_field=False, size_warning=True, verbose_name='cropping')),
                ('content', ckeditor_uploader.fields.RichTextUploadingField()),
                ('organizer', models.CharField(blank=True, max_length=200, null=True)),
                ('commence_date', models.DateTimeField(blank=True, null=True)),
                ('ending_date', models.DateTimeField(blank=True, null=True)),
                ('entry_fee', models.DecimalField(blank=True, decimal_places=0, max_digits=5, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('publish', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('draft', 'draft'), ('publish', 'publish')], default='draft', max_length=10)),
            ],
            options={
                'ordering': ('-publish',),
            },
        ),
    ]
