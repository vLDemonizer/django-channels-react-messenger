import sys

from django.conf import settings

from channels.generic.websocket import AsyncJsonWebsocketConsumer

from asgiref.sync import sync_to_async

from .exceptions import ClientError
from .serializers import MessageSerializer
from .utils import (
    get_chat_or_error, create_message, get_public_key,
    rsa_decrypted_text, aes_decrypted_text
)


class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        if self.scope["user"].is_anonymous:
            await self.close()
        else:
            await self.accept()
        self.chats = set()

    async def receive_json(self, content):
        command = content.get("command", None)
        try:
            if command == "join":
                await self.join_chat(content["chat"])
            elif command == "leave":
                await self.leave_chat(content["chat"])
            elif command == "send":
                await self.send_chat(
                    content["chat"], content["message"], 
                    content['user'], content['type']
                )
        except ClientError as e:
            await self.send_json({"error": e.code})

    async def disconnect(self, code):
        for chat_id in list(self.chats):
            try:
                await self.leave_chat(chat_id)
            except ClientError:
                pass

    ##### Command helper methods called by receive_json

    async def join_chat(self, chat_id):
        # The logged-in user is in our scope thanks to the authentication ASGI middleware
        chat = await get_chat_or_error(chat_id, self.scope["user"])
        public_key = await get_public_key(chat)
        # Store that we're in the chat
        self.chats.add(chat_id)
        # Add them to the group so they get chat messages
        await self.channel_layer.group_add(
            chat.group_name,
            self.channel_name,
        )
        # Instruct their client to finish opening the chat
        await self.send_json({
            "join": str(chat.id),
            "key": str(public_key)
        })

    async def leave_chat(self, chat_id):
        # The logged-in user is in our scope thanks to the authentication ASGI middleware
        chat = await get_chat_or_error(chat_id, self.scope["user"])
        # Remove that we're in the chat
        self.chats.discard(chat_id)
        # Remove them from the group so they no longer get chat messages
        await self.channel_layer.group_discard(
            chat.group_name,
            self.channel_name,
        )
        # Instruct their client to finish closing the chat
        await self.send_json({
            "leave": str(chat.id),
        })

    async def send_chat(self, chat_id, encrypted_message, user, encryption_type):
        if chat_id not in self.chats:
            raise ClientError("chat_ACCESS_DENIED")

        chat = await get_chat_or_error(chat_id, self.scope["user"])
        print(encrypted_message, file=sys.stderr)

        if encryption_type == 'rsa':
            decrypted_message = await rsa_decrypted_text(chat, encrypted_message)
        else:
            decrypted_message = await aes_decrypted_text(encrypted_message)

        print(decrypted_message, file=sys.stderr)
        message = await create_message(chat.id, self.scope["user"], decrypted_message)
        message = MessageSerializer(message).data
        
        await self.channel_layer.group_send(
            chat.group_name,
            {
                "type": "chat.message",
                "chat_id": chat_id,
                "username": self.scope["user"].username,
                "message": message,
            }
        )

    async def chat_join(self, event):
        await self.send_json(
            {
                "chat": event["chat_id"],
                "username": event["username"],
            },
        )

    async def chat_leave(self, event):
        await self.send_json(
            {
                "chat": event["chat_id"],
                "username": event["username"],
            },
        )

    async def chat_message(self, event):
        await self.send_json(
            {
                "chat": event["chat_id"],
                "username": event["username"],
                "message": event["message"],
            },
        )