# Generated by Django 4.2.6 on 2024-03-08 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eLearningApp', '0008_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
