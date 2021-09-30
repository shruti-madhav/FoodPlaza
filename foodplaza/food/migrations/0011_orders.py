# Generated by Django 3.1.4 on 2020-12-28 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0010_auto_20201224_2129'),
    ]

    operations = [
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('orderid', models.AutoField(primary_key=True, serialize=False)),
                ('custemail', models.CharField(max_length=30)),
                ('totalbill', models.IntegerField()),
                ('date', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'Orders',
            },
        ),
    ]