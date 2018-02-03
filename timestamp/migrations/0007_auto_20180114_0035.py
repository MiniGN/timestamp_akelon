# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-01-13 21:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('timestamp', '0006_auto_20180113_1844'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimestampStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.AddField(
            model_name='timestamptask',
            name='status',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='timestamp.TimestampStatus'),
            preserve_default=False,
        ),
    ]
