from channels.db import database_sync_to_async

from .exceptions import ClientError
from .models import Chat, Message


# This decorator turns this function from a synchronous function into an async one
# we can call from our async consumers, that handles Django DBs correctly.
# For more, see http://channels.readthedocs.io/en/latest/topics/databases.html
@database_sync_to_async
def get_chat_or_error(chat_id, user):
    """
    Tries to fetch a chat for the user, checking permissions along the way.
    """
    # Check if the user is logged in
    if not user.is_authenticated:
        raise ClientError("USER_HAS_TO_LOGIN")
    # Find the chat they requested (by ID)
    try:
        chat = Chat.objects.get(pk=chat_id)
    except Chat.DoesNotExist:
        raise ClientError("chat_INVALID")
    return chat

@database_sync_to_async
def create_message(chat_id, user, message):
    if not user.is_authenticated:
        raise ClientError("USER_HAS_TO_LOGIN")
    try:
        chat = Chat.objects.get(pk=chat_id)
    except Chat.DoesNotExist:
        raise ClientError("chat_INVALID")
    message = Message.objects.create(chat=chat, text=message)
    return message
    