"""Module providing chat app logic"""

from django.shortcuts import render, redirect
from django.urls import reverse

from user_app.models import CustomUser
from chat_app.chat_logic import check_if_user_exists
from .chat_logic import generate_room_id
from .models import Message


def home_view(request):
    """Function that renders home.html"""
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
    """Function that generates room id, renders chat.html"""
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


def profile_view(request):
    context = {
        
    }

    user = CustomUser.objects.get(pk=request.user.id)

    if request.method == 'POST':
        data = request.POST
        
        forms = [  # Here we have a list of fields that user wants to change
            data.get('formName', False),
            data.get('formSurname', False),
            data.get('formFamilyname', False),
            data.get('formBio', False),
            data.get('formEmail', False)
        ]

        print('\n', data)
        print(forms)
        
        # user.first_name = forms[0] 

    return render(request, 'profile.html', context)

