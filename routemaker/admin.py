# -*- coding: latin-1 -*-

from django.contrib import admin
from django.contrib.auth.models import User
from models import UserProfile

admin.site.unregister(User)

class UserProfileAdmin(admin.ModelAdmin):
	fields = ('user', 'database')
	search_fields = ['user', 'database']
	list_display = ('user', 'database')
	list_filter = ('user', 'database')

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(User)