# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django import forms
from role.models import *


class RoleGroupForm(forms.ModelForm):
	class Meta:
		model = RoleGroup
		exclude = (
			'role_group_title',
			'role_group_alias',
			'role_group_uuid',
			'role_group_enabled'
		)


class RoleUserForm(forms.ModelForm):
	class Meta:
		model = RoleUser
		exclude = (
			'role_user_username',
			'role_user_password',
			'role_user_group',
			'role_user_email',
			'role_user_firstname',
			'role_user_lastname',
			'role_user_address',
			'role_user_uuid',
			'role_user_enabled'
		)


class RoleSupplierForm(forms.ModelForm):
	class Meta:
		model = RoleSupplier
		exclude = (
			'role_supplier_title',
			'role_supplier_address',
			'role_supplier_user',
			'role_supplier_uuid',
			'role_supplier_enabled'
		)


class RoleUserTokenForm(forms.ModelForm):
	class Meta:
		model = RoleUserToken
		exclude = (
			'role_user_token_user',
			'role_user_token_uuid1',
			'role_user_token_uuid2',
			'role_user_token_start_date',
			'role_user_token_end_date',
			'role_user_token_ip'
		)

