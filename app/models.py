from django.db import models

# Create your models here.
class ChatMessage(models.Model):
    message = models.CharField(max_length=1000)
    room = models.CharField(max_length=100)
