# Generated by Django 3.2.9 on 2021-11-30 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0019_alter_trainingreg_fee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trainingreg',
            name='end_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='trainingreg',
            name='start_date',
            field=models.DateTimeField(),
        ),
    ]
