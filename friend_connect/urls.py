from django.urls import path
from .views import (
    FriendConnectView,
    AcceptFriendConnectView,
    RejectFriendConnectView,
    FriendsListView,
    PendingFriendConnectsView
)


urlpatterns = [
    path(
        'friend-requests/', 
        FriendConnectView.as_view(), 
        name='send-friend-request'
    ),
    path(
        'friend-requests/<int:pk>/accept/', 
        AcceptFriendConnectView.as_view(), 
        name='accept-friend-request'
    ),
    path(
        'friend-requests/<int:pk>/reject/', 
        RejectFriendConnectView.as_view(), 
        name='reject-friend-request'
    ),
    path(
        'friends/', 
        FriendsListView.as_view(), 
        name='friends-list'
    ),
    path(
        'friend-requests/pending/', 
        PendingFriendConnectsView.as_view(), 
        name='pending-friend-requests'
    ),
]