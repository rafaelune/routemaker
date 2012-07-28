from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    database = models.CharField(max_length=256)
    
    def __str__(self):
    	return self.user.username