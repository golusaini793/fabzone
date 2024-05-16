from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from utils.managers import UserManager
from utils.base_model import BaseModel



class User(AbstractBaseUser, PermissionsMixin, BaseModel):
	email = models.EmailField(unique=True)
	name = models.CharField(max_length=32, blank=True)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)
	date_joined = models.DateTimeField(auto_now_add=True)

	objects = UserManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []

	def __str__(self):
		return self.email
