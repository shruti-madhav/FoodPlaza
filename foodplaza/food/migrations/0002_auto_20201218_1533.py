# Generated by Django 3.1.4 on 2020-12-18 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('custname', models.CharField(max_length=20)),
                ('custemail', models.CharField(max_length=20)),
                ('custpass', models.CharField(max_length=20)),
                ('custcontact', models.IntegerField(max_length=10)),
                ('custaddress', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'Customer',
            },
        ),
        migrations.AlterField(
            model_name='food',
            name='foodimg',
            field=models.ImageField(default='', upload_to='media'),
        ),
    ]
