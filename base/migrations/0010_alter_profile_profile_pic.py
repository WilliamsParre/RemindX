# Generated by Django 4.0.5 on 2022-06-06 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_alter_profile_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(blank=True, default='base/static/base/images/default_profile_pic.jpg', upload_to='base/static/base/images/'),
        ),
    ]
