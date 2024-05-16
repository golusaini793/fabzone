# general imports
from __future__ import unicode_literals

# django imports
from django.conf.urls import include
from django.urls import path

# local imports
from authentication.views import (
	UserCreateView,
    UserListView,
    LoginView,
)


urlpatterns = [
	path(
		'signup/',
		UserCreateView.as_view(),
		name='home'
	),
    path(
		'users/',
		UserListView.as_view(),
		name='users'
	),
    path(
        'login/',
        LoginView.as_view(),
        name='login'
    ),
]

