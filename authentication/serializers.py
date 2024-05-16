from django.contrib.auth.models import Group, User
from rest_framework import serializers
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
from django.db.models.functions import Lower
from django.db.models import CharField, EmailField

User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
	name = serializers.CharField(
		required=True,
		max_length=32,
		error_messages={
			"invalid": _("name is required."),
			"blank": _("name is required."),
			"required": _("name is required."),
			"max_length": _("name may not have more than {max_length} characters."),
		}
	)
	email = serializers.EmailField(
		required=True,
		error_messages={
			"invalid": _("Enter a valid email address")
		}
	)
	password = serializers.CharField(write_only=True)

	def validate(self, data):
		try:
			email = data.get("email").lower()
		except:
			email = None

		if not email:
			error_msg = _("Email is required")
			errors = {"error": error_msg}
			raise Exception(error_msg, 400, errors)

		if email:
			EmailField.register_lookup(Lower, "lower")
			email = data.get("email").lower()

			email_exist = User.objects.filter(
				email__lower=email
			)
			if email_exist:
				user_obj = email_exist.first()
				if user_obj:
					email_exists_err_msg = _("Email ID already exists")
					raise serializers.ValidationError(
						{
							"email": email_exists_err_msg
						}
					)

		password = data.get('password')

		if not password:
			password_not_exists_err = _("Password may not be blank")
			errors = {"password": password_not_exists_err}
			raise Exception(password_not_exists_err, 400, errors)

		return data


	def create(self, validated_data):
		user = User(
            email=validated_data['email'],
            name=validated_data['name']
        )
		user.set_password(validated_data.get('password'))
		print("User in searilizer", user)
		user.save()
		return user

	class Meta:
		model = User
		fields = [
			'id',
			'name',
			'email',
			'password'
		]

	def to_representation(self, obj):
		# get the original representation
		response = super().to_representation(obj)

		# return the modified representation
		return response



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email']


class LoginSerializer(serializers.Serializer):
	email = serializers.EmailField(
		required=True,
		error_messages={
			"invalid": _("Enter a valid email address")
		}
	)
	password = serializers.RegexField(
		regex=r'^(?=.*[A-Za-z0-9!@#$&*.]).{8,}$',
		error_messages={
			"invalid": _("Password is invalid."),
			"blank": _("Password may not be blank."),
		},
		required=False,
		allow_blank=True,
		allow_null=True,
		write_only=True
	)
	
	def validate(self, data):
		try:
			email = data.get("email").lower()
		except:
			email = None

		if not email:
			error_msg = _("Email is required")
			errors = {"error": error_msg}
			raise Exception(error_msg, 400, errors)

		if email:
			EmailField.register_lookup(Lower, "lower")
			email = data.get("email").lower()

			email_exist = User.objects.filter(
				email__lower=email
			)
			if not email_exist:
				email_not_exists_err_msg = _("Such User does not exists")
				raise serializers.ValidationError(
					{
						"email": email_not_exists_err_msg
					}
				)
		return data