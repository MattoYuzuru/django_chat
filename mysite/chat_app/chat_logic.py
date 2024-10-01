from django.shortcuts import get_object_or_404
from user_app.models import CustomUser
from .models import Message


def check_if_user_exists(username: str):
    try:
        get_object_or_404(CustomUser, username=username)
        flag = True
    except:
        flag = False

    return flag


def save_message_to_db(sender: str, recipient: str, message: str):
    sender_cu = CustomUser.objects.get(username=sender)
    recipient_cu = CustomUser.objects.get(username=recipient)

    message_obj = Message(sender=sender_cu, recipient=recipient_cu, content=message)
    if Message.objects.last() is not None and message_obj.content == Message.objects.last().content:
        return None

    message_obj.save()


def generate_room_id(username1: str, username2: str):
    room_id = 0
    for char in username1 + username2:
        room_id += ord(char)
    return room_id + len(username1 + username2)
