# Generated by Django 3.1.4 on 2021-01-21 07:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0013_auto_20210120_1733'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ordersummary',
            old_name='foodid',
            new_name='fid',
        ),
    ]
