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
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from pharmacy import encryptor, custom_decorators
import json
import datetime
import os

from django.shortcuts import render

@custom_decorators.admin_required
def filter_pharmacy_articles(request, args):
	object_query = MainDrug.objects.all().order_by('id')

	if request.POST.get('action') == 'search':
		matched_items = []
		search_query = request.POST.get('search_key')

		main_drug_title = object_query.filter(
			main_drug_title__icontains=search_query
		).values_list('id', flat=True)
		for id in main_drug_title:
			matched_items.append(id)

		main_drug_article =object_query.filter(
			main_drug_article__icontains=search_query
		).values_list('id', flat=True)
		for id in main_drug_article:
			matched_items.append(id)

		main_drug_description = object_query.filter(
			main_drug_description__icontains=search_query
		).values_list('id', flat=True)
		for id in main_drug_description:
			matched_items.append(id)

		main_drug_uuid = object_query.filter(
			main_drug_uuid__icontains=search_query
		).values_list('id', flat=True)
		for id in main_drug_uuid:
			matched_items.append(id)

		object_query = MainDrug.objects.filter(
			id__in=matched_items
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
	drugs_list = []
	for drug in query_list:
		title = drug.main_drug_title
		article = drug.main_drug_article
		description = drug.main_drug_description
		uuid = drug.main_drug_uuid
		if request.POST.get('search_key') is not None and len(request.POST.get('search_key')) >= 1:
			highlited_text = '<span style="background:yellow;">' + u''.join(request.POST.get('search_key')) + '</span>'

			title = title.replace(
				request.POST.get('search_key'), highlited_text
			)
			article = article.replace(
				request.POST.get('search_key'), highlited_text
			)
			description = description.replace(
				request.POST.get('search_key'), highlited_text
			)
			uuid = uuid.replace(
				request.POST.get('search_key'), highlited_text
			)
		else:
			pass
		drugs_list.append({
			'id': drug.id,
			'title': title,
			'article': article,
			'description': description,
			'uuid': uuid,
			'enabled': drug.main_drug_uuid,
			'count': int(ResellerDrug.objects.filter(
				reseller_drug_main_id=drug.id
			).count())
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
	params['drug_list'] = drugs_list
	return HttpResponse(json.dumps(params), content_type="application/json")


@custom_decorators.admin_required
def add_edit_pharmacy_articles(request, args):
	params = {}
	try:
		new_main_drug_form = MainDrugForm(request.POST)
		if new_main_drug_form.is_valid:
			try:
				main_drug = new_main_drug_form.save(commit=False)
				main_drug.main_drug_title = request.POST.get('main_drug_title')
				main_drug.main_drug_article = request.POST.get('main_drug_article')
				main_drug.main_drug_description = request.POST.get('main_drug_description')
				new_main_drug_form.save()
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
	return filter_pharmacy_articles(request, args)


@custom_decorators.admin_required
@custom_decorators.assign_session_token
def supplier_pharmacy(request, args):
	args['content'] = 'Dashboard content'
	args['suppliers'] = RoleSupplier.objects.all()
	args['articles'] = MainDrug.objects.all()[0:20]
	response = args['response']
	return response


@custom_decorators.admin_required
def filter_supplier_pharmacy(request, args):
	object_query = ResellerDrug.objects.all().order_by('-id')

	if request.POST.get('action') == 'search':
		matched_items = []
		search_query = request.POST.get('search_key')

		reseller_drug_title = object_query.filter(
			reseller_drug_title__icontains=search_query
		).values_list('id', flat=True)
		for id in reseller_drug_title:
			matched_items.append(id)

		reseller_drug_main =object_query.filter(
			reseller_drug_main__main_drug_title__icontains=search_query
		).values_list('id', flat=True)
		for id in reseller_drug_main:
			matched_items.append(id)

		reseller_drug_dealer = object_query.filter(
			reseller_drug_dealer__role_supplier_title__icontains=search_query
		).values_list('id', flat=True)
		for id in reseller_drug_dealer:
			matched_items.append(id)

		reseller_drug_alias_article = object_query.filter(
			reseller_drug_alias_article__icontains=search_query
		).values_list('id', flat=True)
		for id in reseller_drug_alias_article:
			matched_items.append(id)

		reseller_drug_description = object_query.filter(
			reseller_drug_description__icontains=search_query
		).values_list('id', flat=True)
		for id in reseller_drug_description:
			matched_items.append(id)

		object_query = ResellerDrug.objects.filter(
			id__in=matched_items
		).order_by('-id')
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
	drugs_list = []
	for drug in query_list:

		title = drug.reseller_drug_title
		article = drug.reseller_drug_main.main_drug_title
		alias = drug.reseller_drug_alias_article
		description = drug.reseller_drug_description
		dealer = drug.reseller_drug_dealer.role_supplier_title
		price = drug.reseller_drug_price
		available = drug.reseller_drug_available
		images_set = ResellerDrugImage.objects.filter(
			reseller_drug_image_drug_id__exact=drug.id
		).count()
		drug_uuid = drug.reseller_drug_uuid

		if request.POST.get('search_key_2') is not None and len(request.POST.get('search_key')) >= 1:
			highlited_text = '<span style="background:yellow;">' + u''.join(request.POST.get('search_key')) + '</span>'

			title = title.replace(
				request.POST.get('search_key'), highlited_text
			)
			article = article.replace(
				request.POST.get('search_key'), highlited_text
			)
			alias = alias.replace(
				request.POST.get('search_key'), highlited_text
			)
			description = description.replace(
				request.POST.get('search_key'), highlited_text
			)
			dealer = dealer.replace(
				request.POST.get('search_key'), highlited_text
			)
			drug_uuid = drug_uuid.replace(
				request.POST.get('search_key'), highlited_text
			)
		else:
			pass
		drugs_list.append({
			'id': drug.id,
			'title': title,
			'article': article,
			'alias': alias,
			'description': description,
			'dealer': dealer,
			'price': price,
			'available': available,
			'images_set': images_set,
			'uuid': drug_uuid
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
	params['drug_list'] = drugs_list

	return HttpResponse(json.dumps(params), content_type="application/json")


@custom_decorators.admin_required
def add_edit_supplier_pharmacy(request, args):
	params = {}
	try:
		new_supplier_drug_form = ResellerDrugForm(request.POST)
		if new_supplier_drug_form.is_valid:
			try:
				supplier_drug = new_supplier_drug_form.save(commit=False)
				supplier_drug.reseller_drug_title = request.POST.get('reseller_drug_title')
				supplier_drug.reseller_drug_alias_article = request.POST.get('reseller_drug_alias_article')
				supplier_drug.reseller_drug_main_id = request.POST.get('reseller_drug_main')
				supplier_drug.reseller_drug_description = request.POST.get('reseller_drug_description')
				supplier_drug.reseller_drug_dealer_id = request.POST.get('reseller_drug_dealer')
				supplier_drug.reseller_drug_price = request.POST.get('reseller_drug_price')
				if request.POST.get('reseller_drug_available') == "1":
					supplier_drug.reseller_drug_available = 1
				else:
					supplier_drug.reseller_drug_available = 0
				new_supplier_drug_form.save()

				try:
					for image in request.FILES.getlist('reseller_drug_image'):
						new_supplier_drug_image_form = ResellerDrugImageForm(request.POST, request.FILES)
						if new_supplier_drug_image_form.is_valid:
							drug_image = new_supplier_drug_image_form.save(commit=False)
							drug_image.reseller_drug_image = image
							drug_image.reseller_drug_image_drug_id = supplier_drug.id
							drug_image.save()
						else:
							params['success'] = 'false'
							params['msg_txt'] = 'new_supplier_drug_image_form is not valid'
							return HttpResponse(json.dumps(params), content_type="application/json")
				except:
					pass
			except:
				params['success'] = 'false'
				params['msg_txt'] = 'Error while saving supplier drug'
				return HttpResponse(json.dumps(params), content_type="application/json")
		else:
			params['success'] = 'false'
			params['msg_txt'] = 'new_supplier_drug_form is not valid'
			return HttpResponse(json.dumps(params), content_type="application/json")
	except:
		params['success'] = 'false'
		params['msg_txt'] = 'Error while proceeding of saving reseller drug'
		return HttpResponse(json.dumps(params), content_type="application/json")

	return filter_supplier_pharmacy(request, args)


@custom_decorators.admin_required
def filter_supplier_pharmacy_articles(request, args):
	params = {}
	drugs_list = []

	search_query = request.POST.get('search_key')

	object_query = MainDrug.objects.filter(
		main_drug_title__icontains=search_query
	).order_by('id')[0:30]

	for drug in object_query:
		drugs_list.append({
			'id': drug.id,
			'title': drug.main_drug_title
		})
	params['drugs_list'] = drugs_list

	return HttpResponse(json.dumps(params), content_type="application/json")


@custom_decorators.admin_required
def get_supplier_pharmacy(request, args):
	params = {}
	drug_images = []

	try:
		print (request.POST.get('uuid'))
		drug = ResellerDrug.objects.get(
			reseller_drug_uuid__exact=request.POST.get('uuid')
		)

		images_list = ResellerDrugImage.objects.filter(
			reseller_drug_image_drug_id__exact=drug.id
		)

		print(images_list.count())

		print(drug.id)

		try:
			title = drug.reseller_drug_title
			article = drug.reseller_drug_main.main_drug_title
			article_description = drug.reseller_drug_main.main_drug_description
			alias = drug.reseller_drug_alias_article
			description = drug.reseller_drug_description
			dealer = drug.reseller_drug_dealer.role_supplier_title
			price = drug.reseller_drug_price
			available = drug.reseller_drug_available
			drug_uuid = drug.reseller_drug_uuid
		except:
			params['success'] = "Step 1"
			return HttpResponse(json.dumps(params), content_type="application/json")

		if images_list.count() >= 1:
			for image in images_list:
				try:
					drug_images.append({
						'id': image.id,
						'image': str(image.reseller_drug_image)
					})
				except:
					pass
		else:
			pass

		params['drug_images'] = drug_images
		params['drug_images_count'] = images_list.count()
		params['id'] = drug.id
		params['title'] = title
		params['article'] = article
		params['article_description'] = article_description
		params['alias'] = alias
		params['description'] = description
		params['dealer'] = dealer
		params['price'] = price
		params['available'] = available
		params['uuid'] = drug_uuid
		return HttpResponse(json.dumps(params), content_type="application/json")

	except:
		params['success'] = "false"
		return HttpResponse(json.dumps(params), content_type="application/json")




