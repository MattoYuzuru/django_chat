from django.shortcuts import get_object_or_404
from user_app.models import CustomUser


def check_if_user_exists(username: str):
    try:
        get_object_or_404(CustomUser, username=username)
        flag = True
    except:
        flag = False

    return flag
