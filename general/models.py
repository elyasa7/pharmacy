# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import uuid
from django.db import models

# Create your models here.


class GeneralLanguage(models.Model):
	language_title = models.CharField(
		max_length=50,
		unique=True,
		blank=False,
		null=False
	)
	language_alias = models.CharField(
		max_length=60,
		unique=True,
		blank=False,
		null=False
	)
	language_prefix = models.CharField(
		max_length=2,
		unique=True,
		blank=False,
		null=False
	)
	language_uuid = models.CharField(
		max_length=60,
		default=uuid.uuid4,
		unique=True,
		blank=False,
		null=False
	)
	language_enabled = models.BooleanField(
		default=1,
		blank=False,
		null=False
	)


class GeneralSite(models.Model):
	site_name = models.CharField(
		max_length=50,
		unique=True,
		blank=False,
		null=False
	)
	site_meta_title = models.CharField(
		max_length=250,
		blank=True,
		null=True
	)
	site_meta_description = models.TextField(
		blank=True,
		null=True
	)
	site_meta_keywords = models.CharField(
		max_length=250,
		blank=True,
		null=True
	)
	site_offline = models.BooleanField(
		default=1,
		blank=False,
		null=False
	)
	site_default_listing = models.IntegerField(
		default=20,
		blank=False,
		null=False
	)