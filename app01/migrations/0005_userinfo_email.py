# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2019-04-29 12:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0004_userinfo_pwd'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
    ]