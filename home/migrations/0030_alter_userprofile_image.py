# Generated by Django 3.2.9 on 2022-03-29 03:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0029_auto_20220301_1646'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(blank=True, default='avatar2.jpg', null=True, upload_to='profile'),
        ),
    ]
