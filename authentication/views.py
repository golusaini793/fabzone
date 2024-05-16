# general imports
from __future__ import unicode_literals

# django imports
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

# django rest imports
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


# serializer imports
from authentication.serializers import (
	UserCreateSerializer,
    UserSerializer,
    LoginSerializer,
)


# Create your views here.

User = get_user_model()

class UserCreateView(APIView):
    serializer_class = UserCreateSerializer

    def post(self, request):
        try:
            data = request.data.copy()
            serializer = self.serializer_class(
                data=data
            )
            if serializer.is_valid():
                serializer.save()
                # we can create our own response structer
                return Response(data=serializer.data, status=201)
            else:
                return Response(
                    data=serializer.errors,
                    status=400
                )
        except Exception as error:
            # we can handle this error in better way
            raise error


class LoginView(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserListView(generics.ListAPIView):
    """
    This api work for both listing the users and as well search for the user
    sample : http://localhost:8000/auth/users/ provide list of all user
    http://localhost:8000/auth/users/?search=abc provide user matching with abc
    THis is the implementation by generic view we can't do much modification here
    but we can go with API view if we need to do some other operation
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['=email', '^name']
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]