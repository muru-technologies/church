# Generated by Django 4.1.7 on 2023-04-07 04:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('church', '0006_childdedication_newbeleiver_prayerrequest_testimony'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='childdedication',
            options={'ordering': ('-created',)},
        ),
        migrations.AlterModelOptions(
            name='newbeleiver',
            options={'ordering': ('-created',)},
        ),
        migrations.AlterModelOptions(
            name='prayerrequest',
            options={'ordering': ('-created',)},
        ),
        migrations.AlterModelOptions(
            name='testimony',
            options={'ordering': ('-created',)},
        ),
    ]