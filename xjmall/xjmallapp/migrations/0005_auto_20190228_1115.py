# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-02-28 11:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xjmallapp', '0004_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='good',
            field=models.ManyToManyField(related_name='category_good', to='xjmallapp.Good'),
        ),
    ]
