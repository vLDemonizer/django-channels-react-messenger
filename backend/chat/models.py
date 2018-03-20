from django.db import models
from django.contrib.auth.models import User

class Chat(models.Model):
    """
    A Chat for people to chat in.
    """
    receiver = models.ForeignKey(User, on_delete=None, related_name='user_receiver', blank=True, null=True)
    sender = models.ForeignKey(User, on_delete=None, related_name='user_sender', blank=True, null=True)

    def __str__(self):
        return self.receiver.username + ' - ' + self.sender.username

    @property
    def group_name(self):
        """
        Returns the Channels Group name that sockets should subscribe to to get sent
        messages as they are generated.
        """
        return "chat-%s" % self.id

class Message(models.Model):
    text = models.TextField()
    date_sent = models.DateField(auto_now_add=True)
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=None)