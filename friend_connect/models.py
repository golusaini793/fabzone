from django.db import models
from django.contrib.auth import get_user_model
from utils.base_model import BaseModel

User = get_user_model()

# Create your models here.
class FriendConnect(BaseModel):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    sender = models.ForeignKey(User, related_name='sent_friend_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_friend_requests', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    
    def __str__(self):
        return f'{self.status}'