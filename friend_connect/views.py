from datetime import timedelta
# django imports
from django.contrib.auth import get_user_model
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.utils import timezone

# django rest imports
from rest_framework.views import APIView
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

# local imports
from .models import FriendConnect
from .serializers import FriendConnectSerializer
from authentication.serializers import UserSerializer


User = get_user_model()


class FriendConnectView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = FriendConnectSerializer

    def post(self, request):
        sender = request.user
        receiver = get_object_or_404(User, pk=request.data['receiver'])
        #no more than 3 requests per minute
        one_minute_ago = timezone.now() - timedelta(minutes=1)
        recent_requests = FriendConnect.objects.filter(sender=sender, created_at__gte=one_minute_ago).count()
        if recent_requests >= 3:
            return Response({"detail": "You have exceeded the limit of friend requests. Please try again later."},
                            status=status.HTTP_429_TOO_MANY_REQUESTS)
        ser_data = {
            "sender": sender.pk,
            "receiver": receiver.pk
        }
        serializer = self.serializer_class(data=ser_data)
        if serializer.is_valid():
            serializer.save()
            res_msg = {
                'message': 'Connection request made successfully.',
                'data': serializer.data
            }
            return Response(data=res_msg, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RejectFriendConnectView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        # reject the friend request where receiver is user
        friend_request = get_object_or_404(FriendConnect, pk=pk, receiver=request.user)
        friend_request.status = 'rejected'
        friend_request.save()
        return Response({"status": "Friend request rejected"})
    

class AcceptFriendConnectView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        # accept the friend request where user is receiver.
        friend_request = get_object_or_404(FriendConnect, pk=pk, receiver=request.user)
        friend_request.status = 'accepted'
        friend_request.save()
        return Response({"status": "Friend request accepted"})


class FriendsListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        # extracting all the associated friend req which user sends to other.
        friends = request.user.sent_friend_requests.filter(status="accepted")
        # Extract receiver IDs from the friend requests to show the data of those users
        receiver_ids = friends.values_list('receiver_id', flat=True)
        # Get the receiver user objects
        senders = User.objects.filter(id__in=receiver_ids)
        #paginating the query
        paginator = PageNumberPagination()
        paginated_requests = paginator.paginate_queryset(senders, request)
        serializer = UserSerializer(paginated_requests, many=True)
        return paginator.get_paginated_response(serializer.data)


class PendingFriendConnectsView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        # filtering user friends connects where receiver is user.
        pending_requests = request.user.received_friend_requests.filter(status='pending')
        # pagination
        paginator = PageNumberPagination()
        paginated_requests = paginator.paginate_queryset(pending_requests, request)
        serializer = FriendConnectSerializer(paginated_requests, many=True)
        return paginator.get_paginated_response(serializer.data)