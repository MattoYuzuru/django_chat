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

    message_obj.save()
