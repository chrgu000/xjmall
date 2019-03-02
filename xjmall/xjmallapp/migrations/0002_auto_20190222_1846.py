# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-02-22 18:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xjmallapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='good',
            name='picture_url',
        ),
        migrations.RemoveField(
            model_name='order',
            name='is_check',
        ),
        migrations.RemoveField(
            model_name='order',
            name='is_delivery',
        ),
        migrations.RemoveField(
            model_name='order',
            name='is_revoke',
        ),
        migrations.AddField(
            model_name='order',
            name='order_status',
            field=models.IntegerField(choices=[(0, '\u672a\u5ba1\u6838'), (1, '\u5ba1\u6838\u901a\u8fc7'), (2, '\u5ba1\u6838\u9a73\u56de'), (3, '\u914d\u9001\u5b8c\u6210')], default=0, verbose_name='\u8ba2\u5355\u72b6\u6001'),
        ),
        migrations.AlterField(
            model_name='good',
            name='picture',
            field=models.ImageField(blank=True, default='photo/default.png', null=True, upload_to='photo'),
        ),
    ]