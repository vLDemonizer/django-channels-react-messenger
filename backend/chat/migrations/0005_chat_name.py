# Generated by Django 2.0.3 on 2018-03-30 01:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_auto_20180330_0113'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='name',
            field=models.CharField(default='', max_length=64),
        ),
    ]
