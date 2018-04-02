from django.db import models
from django.contrib.auth.models import User


class Chat(models.Model):
    name = models.CharField(max_length=64, default='')
    users = models.ManyToManyField(User, blank=True)

    def __str__(self):
        description = ''
        for user in self.users.all():
            description += user.username
        return "users: " + description

    @property
    def group_name(self):
        return "chat-%s" % self.id

class Message(models.Model):
    text = models.TextField()
    date_sent = models.DateField(auto_now_add=True)
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=None)
    sender = models.ForeignKey(User, on_delete=None, blank=True, null=True)