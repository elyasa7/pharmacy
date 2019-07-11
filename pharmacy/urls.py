"""pharmacy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from role import views as role_views
from pill import views as pill_views

urlpatterns = [
#   url(r'^admin/', admin.site.urls),
	url(r'^manager/$', role_views.admin_dashboard),
	url(r'^manager/articles/$', role_views.admin_dashboard),
	url(r'^manager/login/$', role_views.admin_login),
	url(r'^manager/login/submit/$', role_views.admin_login_submit),

	url(r'^manager/articles/list/$', pill_views.filter_pharmacy_articles),
	url(r'^manager/articles/add-edit/$', pill_views.add_edit_pharmacy_articles),

	url(r'^manager/admins/$', role_views.admin_manager),
	url(r'^manager/admins/list/$', role_views.filter_admin_users),
	url(r'^manager/admins/add-edit/$', role_views.add_edit_admin_user),

	url(r'^manager/suppliers/$', role_views.supplier_manager),
	url(r'^manager/suppliers/list/$', role_views.filter_supplier_users),
	url(r'^manager/suppliers/add-edit/$', role_views.add_edit_supplier_user),

	url(r'^manager/pharmacies/$', pill_views.supplier_pharmacy),
	url(r'^manager/pharmacies/list/$', pill_views.filter_supplier_pharmacy),
	url(r'^manager/pharmacies/add-edit/$', pill_views.add_edit_supplier_pharmacy),
	url(r'^manager/pharmacies/search-articles/$', pill_views.filter_supplier_pharmacy_articles),
	url(r'^manager/pharmacies/get/$', pill_views.get_supplier_pharmacy),
]
