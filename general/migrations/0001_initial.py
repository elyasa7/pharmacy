# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-01-21 22:14
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GeneralLanguage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_title', models.CharField(max_length=50, unique=True)),
                ('language_alias', models.CharField(max_length=60, unique=True)),
                ('language_prefix', models.CharField(max_length=2, unique=True)),
                ('language_uuid', models.CharField(default=uuid.uuid4, max_length=60, unique=True)),
                ('language_enabled', models.BooleanField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='GeneralSite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_name', models.CharField(max_length=50, unique=True)),
                ('site_meta_title', models.CharField(blank=True, max_length=250, null=True)),
                ('site_meta_description', models.TextField(blank=True, null=True)),
                ('site_meta_keywords', models.CharField(blank=True, max_length=250, null=True)),
                ('site_offline', models.BooleanField(default=1)),
                ('site_default_listing', models.IntegerField(default=20)),
            ],
        ),
    ]
