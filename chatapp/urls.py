from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),            # /
    path("chat/", views.chat_page, name="chat"),  # /chat/
    path("api/chat/", views.chat_api, name="chat_api"),  # ✅ API
]
