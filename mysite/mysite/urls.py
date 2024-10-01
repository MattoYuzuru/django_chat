from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),

    path("user/", include("user_app.urls")),
    path("user/", include("django.contrib.auth.urls")),

    path("home/", include("chat_app.urls")),
]
