# Generated by Django 5.2.1 on 2025-06-01 06:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_flat_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flat',
            name='count',
        ),
    ]
