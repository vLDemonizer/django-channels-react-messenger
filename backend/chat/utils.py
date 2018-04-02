import binascii
import sys

from django.conf import settings

from channels.db import database_sync_to_async

from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from base64 import b64decode

from .exceptions import ClientError
from .models import Chat, Message


@database_sync_to_async
def get_chat_or_error(chat_id, user):
    """
    Tries to fetch a chat for the user, checking permissions along the way.
    """
    if not user.is_authenticated:
        raise ClientError("USER_HAS_TO_LOGIN")
    try:
        chat = Chat.objects.get(pk=chat_id)
    except Chat.DoesNotExist:
        raise ClientError("chat_INVALID")
    return chat

@database_sync_to_async
def create_message(chat_id, user, message):
    """
    Creates a message object to keep on the db for later chat resume.
    """
    if not user.is_authenticated:
        raise ClientError("USER_HAS_TO_LOGIN")
    try:
        chat = Chat.objects.get(pk=chat_id)
    except Chat.DoesNotExist:
        raise ClientError("chat_INVALID")
    message = Message.objects.create(chat=chat, text=message, sender=user)
    return message

def to_string(bytes):
    return bytes.decode("utf-8")

@database_sync_to_async
def get_public_key(chat):
    key_pair = RSA.generate(1024) 
    private_key = to_string(key_pair.exportKey())
    print(private_key, file=sys.stderr)
    private = open("{0}/chat/perms/{1}_private.pem".format(settings.BASE_DIR, chat.name), "w+")
    private.write(private_key)
    private.close()
    public_key = to_string(key_pair.publickey().exportKey())
    print(public_key, file=sys.stderr)
    return public_key

@database_sync_to_async
def rsa_decrypted_text(chat, encrypted_text):
    with open("{0}/chat/perms/{1}_private.pem".format(settings.BASE_DIR, chat.name), "r") as private:
        private_key = private.read()
        key = RSA.importKey(private_key)
        cipher = PKCS1_OAEP.new(key, hashAlgo=SHA256)
        decrypted_message = cipher.decrypt(b64decode(encrypted_text))
    return to_string(decrypted_message)

def _unpad_string(value):
    while value[-1] == '\x00':
        value = value[:-1]
    return value

@database_sync_to_async
def aes_decrypted_text(encrypted_text):
    BLOCK_SIZE = 16
    key = b"1234567890123456"
    encrypted = b64decode(encrypted_text)
    IV = b"this is a passph"
    aes = AES.new(key, AES.MODE_CBC, IV)
    decrypted_text_bytes = aes.decrypt(encrypted[BLOCK_SIZE:])
    decrypted_bytes = decrypted_text_bytes.decode("utf-8")
    return decrypted_bytes
