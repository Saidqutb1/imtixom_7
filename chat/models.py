from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Chat(models.Model):
    participants = models.ManyToManyField(User, related_name='chats')

    def __str__(self):
        return ', '.join([user.username for user in self.participants.all()])


class Message(models.Model):
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='send_message', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} to {self.receiver}: {self.text[:20]}"



