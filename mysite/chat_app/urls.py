from django.urls import path

from . import views

urlpatterns = [
    path("", views.start_chat, name="get_nickname"),
    path("<str:nickname>/", views.chat_view, name="chat"),
]
