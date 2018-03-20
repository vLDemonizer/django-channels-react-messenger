from django.conf import settings

from channels.generic.websocket import AsyncJsonWebsocketConsumer

from .exceptions import ClientError
from .utils import get_chat_or_error, create_message


class ChatConsumer(AsyncJsonWebsocketConsumer):
    """
    This chat consumer handles websocket connections for chat clients.
    It uses AsyncJsonWebsocketConsumer, which means all the handling functions
    must be async functions, and any sync work (like ORM access) has to be
    behind database_sync_to_async or sync_to_async. For more, read
    http://channels.readthedocs.io/en/latest/topics/consumers.html
    """

    ##### WebSocket event handlers

    async def connect(self):
        """
        Called when the websocket is handshaking as part of initial connection.
        """
        # Are they logged in?
        if self.scope["user"].is_anonymous:
            # Reject the connection
            await self.close()
        else:
            # Accept the connection
            await self.accept()
        # Store which chats the user has joined on this connection
        self.chats = set()

    async def receive_json(self, content):
        """
        Called when we get a text frame. Channels will JSON-decode the payload
        for us and pass it as the first argument.
        """
        # Messages will have a "command" key we can switch on
        command = content.get("command", None)
        try:
            if command == "join":
                await self.join_chat(content["chat"])
            elif command == "leave":
                await self.leave_chat(content["chat"])
            elif command == "send":
                await self.send_chat(content["chat"], content["message"])
        except ClientError as e:
            await self.send_json({"error": e.code})

    async def disconnect(self, code):
        """
        Called when the WebSocket closes for any reason.
        """
        # Leave all the chats we are still in
        for chat_id in list(self.chats):
            try:
                await self.leave_chat(chat_id)
            except ClientError:
                pass

    ##### Command helper methods called by receive_json

    async def join_chat(self, chat_id):
        """
        Called by receive_json when someone sent a join command.
        """
        # The logged-in user is in our scope thanks to the authentication ASGI middleware
        chat = await get_chat_or_error(chat_id, self.scope["user"])
        # Store that we're in the chat
        self.chats.add(chat_id)
        # Add them to the group so they get chat messages
        await self.channel_layer.group_add(
            chat.group_name,
            self.channel_name,
        )
        # Instruct their client to finish opening the chat
        if not chat.receiver.username == self.scope["user"].username:
            side = "sender"
        else:
            side = "receiver"
        await self.send_json({
            "join": str(chat.id),
            side: self.scope["user"].username,
        })

    async def leave_chat(self, chat_id):
        """
        Called by receive_json when someone sent a leave command.
        """
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

    async def send_chat(self, chat_id, message):
        """
        Called by receive_json when someone sends a message to a chat.
        """
        # Check they are in this chat
        if chat_id not in self.chats:
            raise ClientError("chat_ACCESS_DENIED")
        # Get the chat and send to the group about it
        chat = await get_chat_or_error(chat_id, self.scope["user"])
        await create_message(chat.id, self.scope["user"], message)
        await self.channel_layer.group_send(
            chat.group_name,
            {
                "type": "chat.message",
                "chat_id": chat_id,
                "username": self.scope["user"].username,
                "message": message,
            }
        )

    ##### Handlers for messages sent over the channel layer

    # These helper methods are named by the types we send - so chat.join becomes chat_join
    async def chat_join(self, event):
        """
        Called when someone has joined our chat.
        """
        # Send a message down to the client
        await self.send_json(
            {
                "chat": event["chat_id"],
                "username": event["username"],
            },
        )

    async def chat_leave(self, event):
        """
        Called when someone has left our chat.
        """
        # Send a message down to the client
        await self.send_json(
            {
                "chat": event["chat_id"],
                "username": event["username"],
            },
        )

    async def chat_message(self, event):
        """
        Called when someone has messaged our chat.
        """
        # Send a message down to the client
        await self.send_json(
            {
                "chat": event["chat_id"],
                "username": event["username"],
                "message": event["message"],
            },
        )