# Generated by Django 3.1 on 2020-08-24 06:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shortener', '0003_auto_20200824_0616'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shortenedurl',
            old_name='source',
            new_name='long_url',
        ),
        migrations.RenameField(
            model_name='shortenedurl',
            old_name='destination',
            new_name='short_url',
        ),
    ]