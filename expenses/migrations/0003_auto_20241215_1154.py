# Generated by Django 3.1.12 on 2024-12-15 08:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0002_auto_20241215_1151'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='expense',
            name='category',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]
