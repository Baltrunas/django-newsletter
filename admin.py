# -*- coding: utf-8 -*
from django.contrib import admin
from newsletter.models import Category
from newsletter.models import Subscriber
from newsletter.models import Mesage


class CategoryAdmin(admin.ModelAdmin):
	list_display = ('name', 'phone', 'from_name', 'from_email', 'public')
	search_fields = ('name', 'phone', 'from_name', 'from_email', 'public')
	list_filter = ('from_email', 'public')
	list_editable = ('public',)

admin.site.register(Category, CategoryAdmin)


class SubscriberAdmin(admin.ModelAdmin):
	list_display = ['name', 'email', 'subscribed', 'key']
	search_fields = ['name', 'email', 'subscribed']
	list_filter = ['subscribed']
	list_editable = ['subscribed']

admin.site.register(Subscriber, SubscriberAdmin)


class MesageAdmin(admin.ModelAdmin):
	list_display = ['subject', 'category', 'created_at']
	search_fields = ['subject', 'category', 'created_at']
	list_filter = ['category']

admin.site.register(Mesage, MesageAdmin)
