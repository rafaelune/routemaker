from django.contrib import admin
from django.contrib.auth.models import User
from models import UserProfile

admin.site.unregister(User)
admin.site.register(UserProfile)
admin.site.register(User)