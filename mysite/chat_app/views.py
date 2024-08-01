from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Message
from user_app.models import CustomUser

from chat_app.chat_logic import check_if_user_exists


def start_chat(request):
    if request.method == 'POST':
        nickname = request.POST.get('recipient_name')
        if nickname and check_if_user_exists(nickname):
            return redirect(reverse('chat', args=[nickname]))
    return redirect('home')


def chat_view(request, nickname):
    sender = request.user
    recipient = CustomUser.objects.get(username=nickname)

    chat = (list(Message.objects.filter(sender=sender.id, recipient=recipient.id)) +
            list(Message.objects.filter(sender=recipient.id, recipient=sender.id)))

    chat.sort(key=lambda x: x.created_at)

    context = {
        "nickname": nickname,
        "messages": chat,
    }

    return render(request, 'chat.html', context)
