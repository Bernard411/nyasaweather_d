# Generated by Django 3.2.13 on 2023-11-26 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_disaster_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='disaster',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='data_images/'),
        ),
    ]
