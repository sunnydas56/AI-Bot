from django.urls import path
from . import views

# app_name = 'myapp'

urlpatterns = [
    path('', views.landing, name='landing'),
    path('signup/', views.signup, name='signup'),
    path('chat/', views.chat_interface, name='chat_interface'),
    path('api/chat/', views.chat_api, name='chat_api'),
]