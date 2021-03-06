# Generated by Django 3.1.4 on 2020-12-31 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0011_orders'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderSummary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('foodid', models.IntegerField()),
                ('orderid', models.IntegerField()),
                ('foodquant', models.IntegerField()),
                ('price', models.FloatField()),
            ],
            options={
                'db_table': 'OrderSummary',
            },
        ),
    ]
