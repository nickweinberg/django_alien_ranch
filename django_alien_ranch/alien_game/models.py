from django.db import models
from django.contrib.auth.models import User

# Create your models here.



class Chat(models.Model):
    users = models.ManyToManyField(User,related_name="chats")

    def __unicode__(self):
        return "Chat Room"


class ChatMessage(models.Model):
    user = models.ForeignKey(User,related_name="chat_messages", blank=True)
    timestamp = models.DateTimeField(auto_now_add=True) 
    chat = models.ForeignKey(Chat, related_name="messages")
    message = models.TextField(max_length=2000,blank=True)

    def __unicode__(self):
        return "Chat message by " + self.user.username