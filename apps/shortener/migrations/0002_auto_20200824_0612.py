# Generated by Django 3.1 on 2020-08-24 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shortener', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shortenedurl',
            name='suggested_path',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='shortenedurl',
            name='destination',
            field=models.CharField(default=None, max_length=512, unique=True),
            preserve_default=False,
        ),
    ]