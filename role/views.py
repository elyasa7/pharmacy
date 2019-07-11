# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# ### Importing models first ### #
from role.models import *
from general.models import *
from pill.models import *

# ### Importing forms ### #
from role.forms import *
from general.forms import *
from pill.forms import *

from django.http import HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from pharmacy import encryptor, custom_decorators
import json
import datetime
import os

from django.shortcuts import render

# Create your views here.


def admin_login(request):
	args={}
	return render(request, "admin/admin_login.html", args)



@csrf_protect
def admin_login_submit(request):
	# args dictionary for front-end variables
	# params dictionary for json response messages
	args = {}
	params = {}

	args['dict'] = custom_decorators.define_language(request)
	if request.POST:
		login = request.POST.get('role_user_username')
		password = request.POST.get('role_user_password')
		enc_password = encryptor.encrypt_json(password)

		try:
			account = RoleUser.objects.get(
				role_user_username__exact=login,
				role_user_password=enc_password
			)
		except:
			account = None

		if account is not None:
			try:
				found_tokens = RoleUserToken.objects.filter(
					role_user_token_user=account
				)
			except:
				found_tokens = None

			if found_tokens.count() >= 1:
				for token in found_tokens:
					token.delete()

			try:
				found_tokens = RoleUserToken.objects.filter(
					role_user_token_user=account
				)
			except:
				found_tokens = None

			# print (found_tokens.count())
			if found_tokens.count() == 0:
				try:
					role_user_token_save_form = RoleUserTokenForm(request.POST)
					if role_user_token_save_form.is_valid:
						try:
							new_token = role_user_token_save_form.save(commit=False)
							new_token.role_user_token_user_id = account.id
							new_token.role_user_token_end_date = datetime.datetime.now()
							new_token.role_user_token_ip = custom_decorators.get_client_ip(request)
							role_user_token_save_form.save()
						except:
							params['success'] = 'false'
							params['msg_txt'] = 'Error while saving token'
							return HttpResponse(json.dumps(params), content_type="application/json")
					else:
						params['success'] = 'false'
						params['msg_txt'] = 'role_user_token_save_form is not valid'
						return HttpResponse(json.dumps(params), content_type="application/json")
				except:
					params['success'] = 'false'
					params['msg_txt'] = 'New token could not be created'
					return HttpResponse(json.dumps(params), content_type="application/json")

				try:
					check_new_token = RoleUserToken.objects.get(
						id__exact=new_token.id
					)
					print (check_new_token.id)
				except:
					check_new_token = None

				if check_new_token is not None:
					token_params = {}
					token_params['id'] = str(
						str(check_new_token.role_user_token_uuid1) + str(
							check_new_token.role_user_token_uuid2)
					)
					token_params['uuid1'] = check_new_token.role_user_token_uuid1
					token_params['uuid2'] = check_new_token.role_user_token_uuid2
					token_params['username'] = check_new_token.role_user_token_user.role_user_username
					token_params['start_date'] = '2018-08-15 13:36:31.676463+00'
					token_params['end_date'] = '2018-08-28 13:36:31.676463+00'
					token_params_json = json.dumps(token_params)
					session_token = encryptor.encrypt_json(token_params_json)
					enc_session_token = encryptor.encrypt_json(session_token)
					response = HttpResponseRedirect('/manager/')
					response.set_cookie('session_token', session_token)
					return response
				else:
					params['success'] = 'false'
					params['msg_txt'] = 'Token could not assigned "check_new_token is None"'
					return HttpResponse(json.dumps(params), content_type="application/json")
			else:
				params['success'] = 'false'
				params['msg_txt'] = 'Token could not assigned'
				return HttpResponse(json.dumps(params), content_type="application/json")
		else:
			params['success'] = 'false'
			params['msg_txt'] = str('Account not found')
			params['user'] = str('Username ' + str(login))
			params['pass'] = str('Password ' + str(password))
			params['encpass'] = str('Encrypted ' + str(enc_password))
			params['account'] = account
			return HttpResponse(json.dumps(params), content_type="application/json")
	else:
		params['success'] = 'false'
		params['msg_txt'] = 'Wrong request method'
		return HttpResponse(json.dumps(params), content_type="application/json")


@custom_decorators.admin_required
def admin_dashboard(request, args):
	args={}
	args['content'] = 'Dashboard content'
	return render(request, "admin/admin_dashboard.html", args)


# ### -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- ### #
# ### ADMINS part - S T A R T E D
# ### -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- ### #


@custom_decorators.admin_required
def admin_manager(request, args):
	args={}
	args['content'] = 'Admin manager'
	return render(request, "admin/admin_manager.html", args)


@custom_decorators.admin_required
def filter_admin_users(request, args):
	object_query = RoleUser.objects.filter(
		role_user_group_id__exact=1
	).order_by('id')

	if request.POST.get('action') == 'search':
		matched_items = []
		search_query = request.POST.get('search_key')

		role_user_username = object_query.filter(
			role_user_username__icontains=search_query
		).values_list('id', flat=True)
		for id in role_user_username:
			matched_items.append(id)

		role_user_email = object_query.filter(
			role_user_email__icontains=search_query
		).values_list('id', flat=True)
		for id in role_user_email:
			matched_items.append(id)

		role_user_firstname = object_query.filter(
			role_user_firstname__icontains=search_query
		).values_list('id', flat=True)
		for id in role_user_firstname:
			matched_items.append(id)

		role_user_lastname = object_query.filter(
			role_user_lastname__icontains=search_query
		).values_list('id', flat=True)
		for id in role_user_lastname:
			matched_items.append(id)

		role_user_address = object_query.filter(
			role_user_address__icontains=search_query
		).values_list('id', flat=True)
		for id in role_user_address:
			matched_items.append(id)

		role_user_uuid = object_query.filter(
			role_user_uuid__icontains=search_query
		).values_list('id', flat=True)
		for id in role_user_uuid:
			matched_items.append(id)

		object_query = RoleUser.objects.filter(
			id__in=matched_items,
			role_user_group_id__exact=1
		).order_by('id')
	else:
		pass

	page_number = request.POST.get('page_number', "1")

	query_page = Paginator(object_query, 10)

	try:
		query_list = query_page.page(page_number)
	except:
		query_list = query_page.page(1)

	index = query_list.number - 1
	max_index = len(query_page.page_range)

	start_index = index - 2 if index >= 2 else 0
	end_index = index + 3 if index <= max_index - 5 else max_index
	page_range = list(query_page.page_range)[start_index:end_index]
	args['query_list'] = query_list

	params={}
	items_list = []
	for item in query_list:
		id = item.id
		username = item.role_user_username
		email = item.role_user_email
		firstname = item.role_user_firstname
		lastname = item.role_user_lastname
		address = item.role_user_address
		uuid = item.role_user_uuid
		enabled = item.role_user_enabled

		items_list.append({
			'id': id,
			'username': username,
			'email': email,
			'firstname': firstname,
			'lastname': lastname,
			'address': address,
			'enabled': enabled,
			'uuid': uuid
		})

	params['all_items_count'] = query_page.count
	params['all_pages_count'] = max_index
	params['pages_has_previous'] = query_list.has_previous()
	params['pages_has_next'] = query_list.has_next()
	try:
		params['previous_page_number'] = query_list.previous_page_number()
	except:
		params['previous_page_number'] = None
	try:
		params['next_page_number'] = query_list.next_page_number()
	except:
		params['next_page_number'] = None
	params['page_range'] = page_range
	params['current_page'] = page_number
	params['search_key'] = request.POST.get('search_key')

	page_range_list = []
	for page in page_range:
		page_range_list.append({
			'page_number': str(page)
		})
	params['page_range'] = page_range_list
	params['items_list'] = items_list
	return HttpResponse(json.dumps(params), content_type="application/json")


@custom_decorators.admin_required
def add_edit_admin_user(request, args):
	params = {}

	role_user_username = request.POST.get('role_user_username')
	role_user_email = request.POST.get('role_user_email')
	role_user_firstname = request.POST.get('role_user_firstname')
	role_user_lastname = request.POST.get('role_user_lastname')
	role_user_address = request.POST.get('role_user_address')

	try:
		user_role_form = RoleUserForm(request.POST)
		if user_role_form.is_valid:
			try:
				if request.POST.get('action') == 'edit_item' and request.POST.get('id') >= 1:
					try:
						user_admin = RoleUser.objects.get(
							id__exact=request.POST.get('id'),
							role_user_group_id__exact=1
						)
						same_usernames = RoleUser.objects.filter(
							role_user_username__exact=request.POST.get('role_user_username')
						).exclude(
							id__exact=user_admin.id
						).count()

						same_emails = RoleUser.objects.filter(
							role_user_email__exact=request.POST.get('role_user_email')
						).exclude(
							id__exact=user_admin.id
						).count()
						if same_emails == 0 and same_usernames == 0 and \
							len(request.POST.get('role_user_username')) >= 1 \
							and len(request.POST.get('role_user_email')) >= 1:
							pass
						else:
							params['success'] = 'false'
							params['msg_txt'] = 'USername or email not valid'
							return HttpResponse(json.dumps(params), content_type="application/json")

					except:
						params['success'] = 'false'
						params['msg_txt'] = 'User with that id not found'
						return HttpResponse(json.dumps(params), content_type="application/json")

					if request.POST.get('edit_password') == '1':
						user_admin.role_user_password = encryptor.encrypt_json(request.POST.get('role_user_password'))
					else:
						pass
				else:
					same_usernames = RoleUser.objects.filter(
						role_user_username__exact=request.POST.get('role_user_username')
					).count()
					same_emails = RoleUser.objects.filter(
						role_user_email__exact=request.POST.get('role_user_email')
					).count()
					try:
						if same_emails == 0 and same_usernames == 0 and \
							len(request.POST.get('role_user_username')) >= 1 \
							and len(request.POST.get('role_user_email')) >= 1:
							pass
						else:
							params['success'] = 'false'
							params['msg_txt'] = 'USername or email not valid'
							return HttpResponse(json.dumps(params), content_type="application/json")
					except:
						params['success'] = 'false'
						params['msg_txt'] = 'Error validating username or email'
						return HttpResponse(json.dumps(params), content_type="application/json")

					user_admin = user_role_form.save(commit=False)
					user_admin.role_user_password=encryptor.encrypt_json(request.POST.get('role_user_password'))

				user_admin.role_user_username = role_user_username
				user_admin.role_user_email = role_user_email
				user_admin.role_user_group_id = 1
				user_admin.role_user_firstname = role_user_firstname
				user_admin.role_user_lastname = role_user_lastname
				user_admin.role_user_address = role_user_address
				user_admin.save()
			except:
				params['success'] = 'false'
				params['msg_txt'] = 'Error while saving main drug'
				return HttpResponse(json.dumps(params), content_type="application/json")
		else:
			params['success'] = 'false'
			params['msg_txt'] = 'new_main_drug_form is not valid'
			return HttpResponse(json.dumps(params), content_type="application/json")
	except:
		params['success'] = 'false'
		params['msg_txt'] = 'New token could not be created'
		return HttpResponse(json.dumps(params), content_type="application/json")
	return filter_admin_users(request, args)

# ### -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- ### #
# ### ADMINS part - E N D
# ### -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- ### #


# ### -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- ### #
# ### SUPPLIERS part - S T A R T E D
# ### -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- ### #

@custom_decorators.admin_required
def supplier_manager(request, args):
	args={}
	args['content'] = 'Suppliers manager'
	return render(request, "admin/supplier_manager.html", args)


@custom_decorators.admin_required
def filter_supplier_users(request, args):
	object_query = RoleSupplier.objects.filter(
		role_supplier_user__role_user_group_id__exact=2
	).order_by('id')

	if request.POST.get('action') == 'search':
		matched_items = []
		search_query = request.POST.get('search_key')

		role_supplier_title = object_query.filter(
			role_supplier_title__icontains=search_query
		).values_list('id', flat=True)
		for id in role_supplier_title:
			matched_items.append(id)

		role_supplier_user__role_user_username = object_query.filter(
			role_supplier_user__role_user_username__icontains=search_query
		).values_list('id', flat=True)
		for id in role_supplier_user__role_user_username:
			matched_items.append(id)

		role_supplier_user__role_user_email = object_query.filter(
			role_supplier_user__role_user_email__icontains=search_query
		).values_list('id', flat=True)
		for id in role_supplier_user__role_user_email:
			matched_items.append(id)

		role_supplier_user__role_user_firstname = object_query.filter(
			role_supplier_user__role_user_firstname__icontains=search_query
		).values_list('id', flat=True)
		for id in role_supplier_user__role_user_firstname:
			matched_items.append(id)

		role_supplier_user__role_user_lastname = object_query.filter(
			role_supplier_user__role_user_lastname__icontains=search_query
		).values_list('id', flat=True)
		for id in role_supplier_user__role_user_lastname:
			matched_items.append(id)

		role_supplier_user__role_user_address = object_query.filter(
			role_supplier_user__role_user_address__icontains=search_query
		).values_list('id', flat=True)
		for id in role_supplier_user__role_user_address:
			matched_items.append(id)

		role_supplier_user__role_user_uuid = object_query.filter(
			role_supplier_user__role_user_uuid__icontains=search_query
		).values_list('id', flat=True)
		for id in role_supplier_user__role_user_uuid:
			matched_items.append(id)

		role_supplier_uuid = object_query.filter(
			role_supplier_uuid__icontains=search_query
		).values_list('id', flat=True)
		for id in role_supplier_uuid:
			matched_items.append(id)

		object_query = RoleSupplier.objects.filter(
			id__in=matched_items,
			role_supplier_user__role_user_group_id__exact=2
		).order_by('id')
	else:
		pass

	page_number = request.POST.get('page_number', "1")

	query_page = Paginator(object_query, 10)

	try:
		query_list = query_page.page(page_number)
	except:
		query_list = query_page.page(1)

	index = query_list.number - 1
	max_index = len(query_page.page_range)

	start_index = index - 2 if index >= 2 else 0
	end_index = index + 3 if index <= max_index - 5 else max_index
	page_range = list(query_page.page_range)[start_index:end_index]
	args['query_list'] = query_list

	params={}
	items_list = []
	for item in query_list:
		id = item.role_supplier_user_id
		title = item.role_supplier_title
		username = item.role_supplier_user.role_user_username
		email = item.role_supplier_user.role_user_email
		firstname = item.role_supplier_user.role_user_firstname
		lastname = item.role_supplier_user.role_user_lastname
		address = item.role_supplier_user.role_user_address
		uuid = item.role_supplier_user.role_user_uuid
		suuid = item.role_supplier_uuid
		enabled = item.role_supplier_enabled

		items_list.append({
			'id': id,
			'title': title,
			'username': username,
			'email': email,
			'firstname': firstname,
			'lastname': lastname,
			'address': address,
			'enabled': enabled,
			'uuid': uuid,
			'suuid': suuid
		})

	params['all_items_count'] = query_page.count
	params['all_pages_count'] = max_index
	params['pages_has_previous'] = query_list.has_previous()
	params['pages_has_next'] = query_list.has_next()
	try:
		params['previous_page_number'] = query_list.previous_page_number()
	except:
		params['previous_page_number'] = None
	try:
		params['next_page_number'] = query_list.next_page_number()
	except:
		params['next_page_number'] = None
	params['page_range'] = page_range
	params['current_page'] = page_number
	params['search_key'] = request.POST.get('search_key')

	page_range_list = []
	for page in page_range:
		page_range_list.append({
			'page_number': str(page)
		})
	params['page_range'] = page_range_list
	params['items_list'] = items_list
	return HttpResponse(json.dumps(params), content_type="application/json")


@custom_decorators.admin_required
def add_edit_supplier_user(request, args):
	params = {}

	role_user_username = request.POST.get('role_user_username')
	role_user_email = request.POST.get('role_user_email')
	role_user_firstname = request.POST.get('role_user_firstname')
	role_user_lastname = request.POST.get('role_user_lastname')
	role_user_address = request.POST.get('role_user_address')
	role_user_supplier_title = request.POST.get('role_user_supplier_title')

	try:
		user_role_form = RoleUserForm(request.POST)
		if user_role_form.is_valid:
			try:
				if request.POST.get('action') == 'edit_item' and request.POST.get('id') >= 1:
					try:
						user_supplier = RoleUser.objects.get(
							id__exact=request.POST.get('id'),
							role_user_group_id__exact=2
						)
						same_usernames = RoleUser.objects.filter(
							role_user_username__exact=request.POST.get('role_user_username')
						).exclude(
							id__exact=user_supplier.id
						).count()

						same_emails = RoleUser.objects.filter(
							role_user_email__exact=request.POST.get('role_user_email')
						).exclude(
							id__exact=user_supplier.id
						).count()
						if same_emails == 0 and same_usernames == 0 and \
							len(request.POST.get('role_user_username')) >= 1 \
							and len(request.POST.get('role_user_email')) >= 1 \
							and len(request.POST.get('role_user_supplier_title')) >= 1:
							pass
						else:
							params['success'] = 'false'
							params['msg_txt'] = 'Username or email not valid in editing'
							return HttpResponse(json.dumps(params), content_type="application/json")

					except:
						params['success'] = 'false'
						params['msg_txt'] = 'User with that id not found'
						return HttpResponse(json.dumps(params), content_type="application/json")

					if request.POST.get('edit_password') == '1':
						user_supplier.role_user_password = encryptor.encrypt_json(request.POST.get('role_user_password'))
					else:
						pass
				else:
					same_usernames = RoleUser.objects.filter(
						role_user_username__exact=request.POST.get('role_user_username')
					).count()
					same_emails = RoleUser.objects.filter(
						role_user_email__exact=request.POST.get('role_user_email')
					).count()
					try:
						if same_emails == 0 and same_usernames == 0 and \
							len(request.POST.get('role_user_username')) >= 1 \
							and len(request.POST.get('role_user_email')) >= 1 \
							and len(request.POST.get('role_user_supplier_title')) >= 1:
							pass
						else:
							params['success'] = 'false'
							params['msg_txt'] = 'USername or email not valid'
							params['count'] = str(same_usernames) + ' ' + str(same_emails)
							return HttpResponse(json.dumps(params), content_type="application/json")
					except:
						params['success'] = 'false'
						params['msg_txt'] = 'Error validating username or email'
						return HttpResponse(json.dumps(params), content_type="application/json")

					user_supplier = user_role_form.save(commit=False)
					user_supplier.role_user_password=encryptor.encrypt_json(request.POST.get('role_user_password'))

				user_supplier.role_user_username = role_user_username
				user_supplier.role_user_email = role_user_email
				user_supplier.role_user_group_id = 2
				user_supplier.role_user_firstname = role_user_firstname
				user_supplier.role_user_lastname = role_user_lastname
				user_supplier.role_user_address = role_user_address
				user_supplier.save()

				try:
					role_supplier_user = RoleUser.objects.get(
						id__exact=user_supplier.id,
						role_user_group_id__exact=2
					)
				except:
					params['success'] = 'false'
					params['msg_txt'] = 'role_supplier_user error'
					return HttpResponse(json.dumps(params), content_type="application/json")

				try:

					if request.POST.get('action') == 'edit_item':
						user_supplier = RoleSupplier.objects.get(
							role_supplier_user_id__exact=role_supplier_user.id
						)

						user_supplier.role_supplier_title = role_user_supplier_title
						user_supplier.save(update_fields=['role_supplier_title'])
					else:
						user_supplier_form = RoleSupplierForm(request.POST)
						if user_supplier_form.is_valid:
							new_user_supplier = user_supplier_form.save(commit=False)
							new_user_supplier.role_supplier_user_id = role_supplier_user.id
							new_user_supplier.role_supplier_title = role_user_supplier_title
							new_user_supplier.save()
						else:
							if request.POST.get('action') == 'edit_item':
								pass
							else:
								try:
									user_supplier.delete()
								except:
									pass
							params['success'] = 'false'
							params['msg_txt'] = 'Error while saving supplier user, user_supplier_form not valid'
							return HttpResponse(json.dumps(params), content_type="application/json")
				except:
					if request.POST.get('action') == 'edit_item':
						pass
					else:
						try:
							user_supplier.delete()
						except:
							pass
					params['success'] = 'false'
					params['msg_txt'] = 'Error while saving supplier user'
					return HttpResponse(json.dumps(params), content_type="application/json")
			except:
				params['success'] = 'false'
				params['msg_txt'] = 'Saving supplier failed'
				return HttpResponse(json.dumps(params), content_type="application/json")
		else:
			params['success'] = 'false'
			params['msg_txt'] = 'user_role_form is not valid'
			return HttpResponse(json.dumps(params), content_type="application/json")
	except:
		params['success'] = 'false'
		params['msg_txt'] = 'New token could not be created'
		return HttpResponse(json.dumps(params), content_type="application/json")
	return filter_admin_users(request, args)

# ### -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- ### #
# ### SUPPLIERS part - E N D S
# ### -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- ### #