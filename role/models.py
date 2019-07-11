# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import uuid

# Create your models here.


class RoleGroup(models.Model):
	class Meta:
		db_table = "role_group"
		ordering = ['-id']

	role_group_title = models.CharField(
		max_length=50,
		unique=True,
		blank=False,
		null=False
	)
	role_group_alias = models.CharField(
		max_length=60,
		unique=True,
		blank=False,
		null=False
	)
	role_group_uuid = models.CharField(
		max_length=36,
		default=uuid.uuid4,
		unique=True,
		blank=False,
		null=False
	)
	role_group_enabled = models.BooleanField(
		default=1,
		blank=False,
		null=False
	)


class RoleUser(models.Model):
	class Meta:
		db_table = "role_user"
		ordering = ['-id']

	role_user_username = models.CharField(
		max_length=50,
		unique=True,
		blank=False,
		null=False
	)
	role_user_password = models.CharField(
		max_length=300,
		blank=False,
		null=False
	)
	role_user_group = models.ForeignKey(
		'RoleGroup',
		related_name="role_user_group",
		on_delete=models.CASCADE,
		blank=False,
		null=False
	)
	role_user_email = models.CharField(
		max_length=60,
		unique=True,
		blank=False,
		null=False
	)
	role_user_firstname = models.CharField(
		max_length=60,
		unique=True,
		blank=False,
		null=False
	)
	role_user_lastname = models.CharField(
		max_length=60,
		unique=True,
		blank=False,
		null=False
	)
	role_user_address = models.CharField(
		max_length=600,
		unique=True,
		blank=False,
		null=False
	)
	role_user_uuid = models.CharField(
		max_length=36,
		default=uuid.uuid4,
		unique=True,
		blank=False,
		null=False
	)
	role_user_enabled = models.BooleanField(
		default=1,
		blank=False,
		null=False
	)


class RoleSupplier(models.Model):
	class Meta:
		db_table = "role_supplier"
		ordering = ['-id']
		indexes = [
			models.Index(
				fields=[
					'role_supplier_title',
					'role_supplier_address'
				]
			)
		]

	role_supplier_title = models.CharField(
		max_length=150,
		blank=False,
		null=False
	)
	role_supplier_address = models.CharField(
		max_length=200,
		blank=False,
		null=False
	)
	role_supplier_user = models.ForeignKey(
		'RoleUser',
		related_name="role_supplier_user_key",
		on_delete=models.CASCADE,
		blank=False,
		null=False
	)
	role_supplier_uuid = models.CharField(
		max_length=36,
		default=uuid.uuid4,
		unique=True,
		blank=False,
		null=False
	)
	role_supplier_enabled = models.BooleanField(
		default=1,
		blank=False,
		null=False
	)


class RoleUserToken(models.Model):
	class Meta():
		db_table = "role_user_token"

	role_user_token_user = models.ForeignKey(
		'RoleUser',
		related_name="role_user_token_user_key",
		on_delete=models.CASCADE,
		blank=False,
		null=False,
	)

	role_user_token_uuid1 = models.CharField(
		max_length=36,
		unique=True,
		default=uuid.uuid4,
		blank=False,
		null=False,
	)

	role_user_token_uuid2 = models.CharField(
		max_length=36,
		unique=True,
		default=uuid.uuid4,
		blank=False,
		null=False,
	)

	role_user_token_start_date = models.DateTimeField(
		auto_now_add=True,
		blank=False,
		null=False,
	)

	role_user_token_end_date = models.DateTimeField(
		blank=False,
		null=False,
	)

	role_user_token_ip = models.CharField(
		max_length=16,
		blank=False,
		null=False,
	)
