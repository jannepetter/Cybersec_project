from django.urls import path

from .views import homeView, messageView,sendMessageView,allMessageView

urlpatterns = [
    path("home", homeView, name="home"),
    path("messages", messageView, name="messages"),
    path("allmessages", allMessageView, name="allmessages"),
    path("send", sendMessageView, name="send"),
]