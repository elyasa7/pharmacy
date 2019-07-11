# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import uuid
import os

from django.db import models
from role.models import RoleSupplier

from slugify import slugify, Slugify, UniqueSlugify
# Create your models here.


def get_upload_path(self, filename):
	upload_path = os.path.join('media/pharmacy',
		str(self.reseller_drug_image_drug.reseller_drug_dealer.id),
		str(self.reseller_drug_image_drug.id),
	)
	if not os.path.exists(upload_path):
		os.makedirs(upload_path)
	return os.path.join(upload_path, slugify(u''.join(filename), to_lower=True))


class MainDrug(models.Model):
	class Meta:
		db_table = "main_drug"
		ordering = ['-id']
		indexes = [
			models.Index(
				fields=[
					'main_drug_title',
					'main_drug_article',
					'main_drug_description'
				]
			)
		]

	main_drug_title = models.CharField(
		max_length=100,
		blank=False,
		null=False,
	)
	main_drug_article = models.CharField(
		max_length=100,
		unique=True,
		blank=False,
		null=False,
	)
	main_drug_description = models.TextField(
		blank=True,
		null=True,
	)
	main_drug_prescription = models.BooleanField(
		default=0,
		blank=False,
		null=False,
	)
	main_drug_uuid = models.CharField(
		max_length=36,
		default=uuid.uuid4,
		blank=False,
		null=False,
		unique=True,
	)


class ResellerDrug(models.Model):
	class Meta:
		db_table = "reseller_drug"
		ordering = ['-id']
		indexes = [
			models.Index(
				fields=[
					'reseller_drug_title',
					'reseller_drug_alias_article',
					'reseller_drug_description',
					'reseller_drug_price',
				]
			)
		]

	reseller_drug_title = models.CharField(
		max_length=100,
		blank=False,
		null=False,
	)
	reseller_drug_main = models.ForeignKey(
		'MainDrug',
		related_name="reseller_drug_main_key",
		on_delete=models.CASCADE,
		blank=False,
		null=False,
	)
	reseller_drug_dealer = models.ForeignKey(
		'role.RoleSupplier',
		related_name="reseller_drug_dealer_key",
		on_delete=models.CASCADE,
		blank=False,
		null=False,
	)
	reseller_drug_alias_article = models.CharField(
		max_length=100,
		unique=True,
		blank=False,
		null=False,
	)
	reseller_drug_description = models.TextField(
		blank=True,
		null=True,
	)
	reseller_drug_price = models.FloatField(
		blank=False,
		null=False,
	)
	reseller_drug_available = models.BooleanField(
		default=0,
		blank=False,
		null=False,
	)
	reseller_drug_uuid = models.CharField(
		max_length=36,
		default=uuid.uuid4,
		blank=False,
		null=False,
		unique=True,
	)


class ResellerDrugImage(models.Model):
	class Meta:
		db_table = "reseller_drug_image"
		ordering = ['-id']

	reseller_drug_image = models.ImageField(
		upload_to=get_upload_path,
		blank=False,
		null=False,
	)
	reseller_drug_image_drug = models.ForeignKey(
		'ResellerDrug',
		related_name="reseller_drug_image_drug_key",
		on_delete=models.CASCADE,
		blank=False,
		null=False,
	)
	reseller_drug_image_created = models.DateTimeField(
		auto_now_add=True,
		blank=False,
		null=False,
	)
	reseller_drug_image_main = models.BooleanField(
		default=0,
		blank=False,
		null=False,
	)
	main_drug_image_uuid = models.CharField(
		max_length=36,
		default=uuid.uuid4,
		blank=False,
		null=False,
		unique=True,
	)