# general imports
from __future__ import unicode_literals

# django imports
from django.db import models
# from django.utils.translation import ugettext_lazy as _
from django.utils.translation import gettext_lazy as _


# Create your base model here.


class BaseModel(models.Model):
	'''
		Base model for created_at and updated_at field
	'''
	created_at = models.DateTimeField(_('date joined'), auto_now_add=True)
	updated_at = models.DateTimeField(_('date update'), auto_now=True)

	class Meta:
		abstract=True

