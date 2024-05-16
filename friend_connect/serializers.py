from rest_framework import serializers
from .models import FriendConnect


class FriendConnectSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendConnect
        fields = ['id', 'sender', 'receiver', 'status']