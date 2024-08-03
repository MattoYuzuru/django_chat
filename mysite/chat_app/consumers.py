import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from .chat_logic import save_message_to_db, generate_room_id
from .models import Message

from user_app.models import CustomUser


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_group_name = f"chat_{self.room_id}"

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        sender = text_data_json["sender"]
        recipient = text_data_json["recipient"]

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "sender": sender,
                "recipient": recipient,
            },
        )

    def chat_message(self, event):
        message = event["message"]
        sender = event["sender"]
        recipient = event["recipient"]

        self.send(text_data=json.dumps({"message": message, "sender": sender, "recipient": recipient}))

        if message:
            save_message_to_db(sender, recipient, message)