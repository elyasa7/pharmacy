# -*- coding:utf-8 -*-

from __future__ import unicode_literals

from django.shortcuts import render

from role.models import *
from django.http import HttpResponseRedirect
from pharmacy import encryptor
import json

#args = {}


def define_language(request):
	args = {}
	try:
		dict_set = request.COOKIES.get('language')
	except:
		dict_set = None

	if dict_set == 'ru':
		args['dict'] = dict_set
		pass
	else:
		args['dict'] = 'en'
		pass


def get_client_ip(request):
	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

	if x_forwarded_for:
		ip = x_forwarded_for.split(',')[0]
	else:
		ip = request.META.get('REMOTE_ADDR')
	return ip


def token_required(view_func):
	def check_token_validation(request, args={}):
		args = {}
		try:
			token = request.COOKIES.get('session_token')
		except:
			token = None
		if token is None:
			return HttpResponseRedirect('/manager/login/')
		else:
			pass

		try:
			dec_token = encryptor.decrypt_json(token)
		except:
			dec_token = None
		if dec_token is None:
			return HttpResponseRedirect('/manager/login/')
		else:
			pass

		try:
			dec_token_json = json.loads(dec_token)
		except:
			dec_token_json = None
		if dec_token_json is None:
			return HttpResponseRedirect('/manager/login/')
		else:
			pass

		try:
			valid_token = RoleUserToken.objects.get(
				role_user_token_uuid1__exact=str(dec_token_json['uuid1']),
				role_user_token_uuid2__exact=str(dec_token_json['uuid2']),
				role_user_token_user__role_user_username__exact=str(dec_token_json['username']),
				role_user_token_user__role_user_enabled__exact=1
			)
		except:
			valid_token = None
		if valid_token is None:
			return HttpResponseRedirect('/manager/login/')
		else:
			args['token_account'] = RoleUser.objects.get(
				role_user_username__exact=str(dec_token_json['username'])
			)
			return view_func(request, args)

	return check_token_validation



def admin_required(view_func):
	def check_token_validation(request, args={}):
		args = {}
		try:
			token = request.COOKIES.get('session_token')
		except:
			token = None
		if token is None:
			return HttpResponseRedirect('/manager/login/')
		else:
			pass

		try:
			dec_token = encryptor.decrypt_json(token)
		except:
			dec_token = None
		if dec_token is None:
			return HttpResponseRedirect('/manager/login/')
		else:
			pass

		try:
			dec_token_json = json.loads(dec_token)
		except:
			dec_token_json = None
		if dec_token_json is None:
			return HttpResponseRedirect('/manager/login/')
		else:
			pass

		try:
			valid_token = RoleUserToken.objects.get(
				role_user_token_uuid1__exact=str(dec_token_json['uuid1']),
				role_user_token_uuid2__exact=str(dec_token_json['uuid2']),
				role_user_token_user__role_user_username__exact=str(dec_token_json['username']),
				role_user_token_user__role_user_enabled__exact=1
			)
		except:
			valid_token = None
		if valid_token is None:
			return HttpResponseRedirect('/manager/login/')
		else:
			pass

		try:
			admin_user = RoleUser.objects.get(
				role_user_username__exact=str(dec_token_json['username']),
				role_user_group_id__exact=1
			)
		except:
			admin_user = None

		if admin_user is None:
			return HttpResponseRedirect('/manager/login/')
		else:
			args['token_account'] = (admin_user)
			return view_func(request, args)

	return check_token_validation


def token_required(view_func):
	def check_token_validation(request, args={}):
		args = {}
		try:
			token = request.COOKIES.get('session_token')
		except:
			token = None
		if token is None:
			return HttpResponseRedirect('/manager/login/')
		else:
			pass

		try:
			dec_token = encryptor.decrypt_json(token)
		except:
			dec_token = None
		if dec_token is None:
			return HttpResponseRedirect('/manager/login/')
		else:
			pass

		try:
			dec_token_json = json.loads(dec_token)
		except:
			dec_token_json = None
		if dec_token_json is None:
			return HttpResponseRedirect('/manager/login/')
		else:
			pass

		try:
			valid_token = RoleUserToken.objects.get(
				role_user_token_uuid1__exact=str(dec_token_json['uuid1']),
				role_user_token_uuid2__exact=str(dec_token_json['uuid2']),
				role_user_token_user__role_user_username__exact=str(dec_token_json['username']),
				role_user_token_user__role_user_enabled__exact=1
			)
		except:
			valid_token = None
		if valid_token is None:
			return HttpResponseRedirect('/manager/login/')
		else:
			args['token_account'] = RoleUser.objects.get(
				role_user_username__exact=str(dec_token_json['username'])
			)
			return view_func(request, args)

	return check_token_validation


def assign_session_token(view_func):
	def check_session_token(request, args={}):
		args = {}
		args['response'] = response = render(request, "admin/supplier_pharmacy.html", args)
		try:
			once_token = request.COOKIES.get('once_token')
		except:
			once_token = None

		if once_token is None:
			response.set_cookie('once_token', str(str(uuid.uuid4()) + str(uuid.uuid4())))
		else:
			pass
		return view_func(request, args)

	return check_session_token
