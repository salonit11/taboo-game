from chat import views as chat_views
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import include, path

urlpatterns = [
    path("", chat_views.chatPage, name="chat-page"),
    path("get_word_data/", chat_views.get_word_data, name="get_word_data"),
    path("register/", chat_views.register, name="register"),
    path(
        "auth/login/",
        LoginView.as_view(template_name="chat/LoginPage.html"),
        name="login-user",
    ),
    path("auth/logout/", LogoutView.as_view(), name="logout-user"),
]
