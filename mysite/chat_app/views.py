from django.shortcuts import render, redirect
from django.urls import reverse

from .chat_logic import generate_room_id
from .models import Message
from user_app.models import CustomUser

from chat_app.chat_logic import check_if_user_exists


def home_view(request):
    curr_user = request.user.id
    users = CustomUser.objects.exclude(id=curr_user)
    chats = []

    for user in users:
        message = Message.objects.filter(sender=curr_user, recipient=user.id).exists()
        if message:
            chats.append(user.username)

    if request.method == 'POST':
        nickname = request.POST.get('recipient_name')
        if nickname and check_if_user_exists(nickname) and str(request.user) != nickname:
            return redirect(reverse('chat', args=[nickname]))

    context = {
        'all_chats': chats,
    }

    return render(request, 'home.html', context)


def chat_view(request, nickname):
    sender = request.user
    recipient = CustomUser.objects.get(username=nickname)

    room_id = generate_room_id(sender.username, recipient.username)

    chat = (list(Message.objects.filter(sender=sender.id, recipient=recipient.id)) +
            list(Message.objects.filter(sender=recipient.id, recipient=sender.id)))

    chat.sort(key=lambda x: x.created_at)

    context = {
        "room_id": room_id,
        "nickname": nickname,
        "messages": chat,
    }

    return render(request, 'chat.html', context)
