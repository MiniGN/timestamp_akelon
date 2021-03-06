# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-01-14 13:38
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('timestamp', '0008_auto_20180114_1631'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuartalTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('executor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Квартальная задача',
                'verbose_name_plural': 'Квартальные задачи',
            },
        ),
        migrations.AddField(
            model_name='projecttask',
            name='executor',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
