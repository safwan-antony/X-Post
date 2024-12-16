from django.urls import path
from .views import *

urlpatterns = [
    path('private/<int:pk>/',message_chat , name='message_chat'),
    path('groop_rooms/',groop_rooms , name='groop_rooms'),
    path('create_room/',create_room,name='create_room'),
    path('<slug:slug>/',room_chat,name='room_chat'),
]