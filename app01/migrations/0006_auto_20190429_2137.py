# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2019-04-29 13:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0005_userinfo_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='userinfo',
            name='mobile',
            field=models.CharField(max_length=11, null=True),
        ),
    ]
