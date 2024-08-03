from django.db import models

from user_app.models import CustomUser


class Message(models.Model):
    sender = models.ForeignKey(CustomUser, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(CustomUser, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender} to {self.recipient}: "{self.content[:10]}..."'


class ChatRoom(models.Model):
    users = models.ManyToManyField(CustomUser)
    room_id = models.CharField(max_length=300, unique=True)

    def __str__(self):
        return self.room_id
