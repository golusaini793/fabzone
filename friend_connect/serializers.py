from rest_framework import serializers
from .models import FriendConnect


class FriendConnectSerializer(serializers.ModelSerializer):
    sender_email = serializers.EmailField(source='sender.email', read_only=True)
    receiver_email = serializers.EmailField(source='receiver.email', read_only=True)
    
    class Meta:
        model = FriendConnect
        fields = ['id', 'sender', 'receiver', 'status', 'sender_email', 'receiver_email']