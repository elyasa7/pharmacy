# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django import forms
from pill.models import *


class MainDrugForm(forms.ModelForm):
	class Meta:
		model = MainDrug
		exclude = (
			'main_drug_title',
			'main_drug_article',
			'main_drug_description',
			'main_drug_prescription',
			'main_drug_uuid',
		)


class ResellerDrugForm(forms.ModelForm):
	class Meta:
		model = ResellerDrug
		exclude = (
			'reseller_drug_title',
			'reseller_drug_main',
			'reseller_drug_dealer',
			'reseller_drug_alias_article',
			'reseller_drug_description',
			'reseller_drug_price',
			'reseller_drug_available',
			'reseller_drug_uuid'
		)


class ResellerDrugImageForm(forms.ModelForm):
	class Meta:
		model = ResellerDrugImage
		exclude = (
			'reseller_drug_image',
			'reseller_drug_image_drug',
			'reseller_drug_image_created',
			'reseller_drug_image_main',
			'main_drug_image_uuid'
		)