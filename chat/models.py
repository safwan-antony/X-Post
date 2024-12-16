from django.db import models
from a_users.models import User
# Create your models here.



class MessageChat(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='host' , null=True)
    friend_chat = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_chat' , null=True)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message[0:50]
    
class GroopRooms(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner' , null=True)
    participants = models.ManyToManyField(User,related_name='participants',blank=True )
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100,unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class RoomChat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user' , null=True)
    room = models.ForeignKey(GroopRooms, on_delete=models.CASCADE, related_name='room' , null=True)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}: {self.message[:20]}..."
    
