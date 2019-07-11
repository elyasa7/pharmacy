# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django import forms
from general.models import *


class GeneralLanguageForm(forms.ModelForm):
	class Meta:
		model = GeneralLanguage
		exclude = (
			'language_title',
			'language_alias',
			'language_prefix',
			'language_uuid',
			'language_enabled',
		)


class GeneralSiteForm(forms.ModelForm):
	class Meta:
		model = GeneralSite
		exclude = (
			'site_name',
			'site_meta_title',
			'site_meta_description',
			'site_meta_keywords',
			'site_offline',
			'site_default_listing',
		)