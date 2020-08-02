from django.urls import path
from .views import UserRegisterView


urlpatterns = [
    path('register/', UserRegisterView.as_view(), name="register"),
    # path('login', views.login, name="login"), 
    # path('register', views.register, name = "register")
]

